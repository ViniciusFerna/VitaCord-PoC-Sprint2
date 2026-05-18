from typing import TypedDict, Annotated, List, Optional
from langgraph.graph import StateGraph, END
import operator
import ollama
import json
from src.rag.retriever import recuperar_contexto
from src.agents.guardrails import detectar_red_flag, detectar_fora_escopo, validar_saida, RESPOSTA_FORA_ESCOPO, RESPOSTA_EMERGENCIA
from src.agents.SysPrompt import montar_system_prompt
from src.tools.definitions import tools
from src.tools.dispatcher import executar_tool


# --- ESTADO COMPARTILHADO ---
class EstadoClinico(TypedDict):
    mensagens: Annotated[List[dict], operator.add]
    paciente_id: str
    contexto_rag: str
    intencao: str
    resposta_final: str
    escalada: bool
    tools_chamadas: list


MODEL = "qwen3.5:9b"


# --- NÓ: SUPERVISOR ---
def no_supervisor(estado: EstadoClinico) -> EstadoClinico:
    """
    Classifica a intenção da última mensagem do usuário.
    Retorna: triagem | prescricao | escalada
    """
    ultima_msg = estado["mensagens"][-1]["content"]

    # Guardrail de red flag ANTES do LLM
    if detectar_red_flag(ultima_msg):
        return {**estado, "intencao": "escalada", "escalada": True}

    # Guardrail de escopo
    if detectar_fora_escopo(ultima_msg):
        return {**estado, "intencao": "fora_escopo", "escalada": False}

    # Classificação por LLM
    prompt_classificacao = f"""Classifique a intenção abaixo em uma palavra APENAS:
- triagem: relato de sintomas, medições, bem-estar, consulta de histórico
- prescricao: menciona medicamentos, quer saber sobre tratamento, pede prescrição
- escalada: sintomas graves de emergência
- fora_escopo: qualquer assunto não relacionado à saúde ou ao sistema CarePlus

Responda APENAS com uma das quatro palavras, sem pontuação.

Mensagem: {ultima_msg}"""

    resposta = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt_classificacao}],
        options={"temperature": 0.0}
    )
    intencao = resposta["message"]["content"].strip().lower()

    # Normaliza para evitar variações
    if "escala" in intencao:
        intencao = "escalada"
    elif "prescri" in intencao:
        intencao = "prescricao"
    elif "escopo" in intencao or "fora" in intencao:
        intencao = "fora_escopo"
    else:
       intencao = "triagem"

    return {**estado, "intencao": intencao, "escalada": intencao == "escalada"}


# --- NÓ: TRIAGEM ---
def no_triagem(estado: EstadoClinico) -> EstadoClinico:
    """Coleta dados do paciente com RAG enriquecendo o contexto."""
    ultima_msg = estado["mensagens"][-1]["content"]

    # RAG: recupera contexto relevante
    contexto_rag = recuperar_contexto(ultima_msg, n_resultados=2)

    system_prompt = montar_system_prompt(contexto_rag)
    mensagens_llm = [{"role": "system", "content": system_prompt}] + estado["mensagens"]

    tools_registradas = []

    while True:
        resposta = ollama.chat(
            model=MODEL,
            messages=mensagens_llm,
            tools=tools,
            options={"temperature": 0.3, "top_p": 0.9}
        )
        msg = resposta["message"]

        if msg.get("tool_calls"):
            mensagens_llm.append(msg)
            for tc in msg["tool_calls"]:
                nome = tc["function"]["name"]
                args = tc["function"]["arguments"]

                # Registra a tool chamada
                tools_registradas.append({
                    "nome": nome,
                    "argumentos": args
                })

                resultado = executar_tool(tc["function"]["name"], tc["function"]["arguments"])
                mensagens_llm.append({"role": "tool", "content": resultado})
            continue

        texto = msg["content"]
        valido, texto_final = validar_saida(texto)
        break

    nova_msg = {"role": "assistant", "content": texto_final}
    return {**estado, "mensagens": [nova_msg], "contexto_rag": contexto_rag, "resposta_final": texto_final, "tools_chamadas": tools_registradas}


# --- NÓ: PRESCRIÇÃO ---
def no_prescricao(estado: EstadoClinico) -> EstadoClinico:
    """Redireciona tentativas de prescrição para o médico."""
    resposta = (
        "Entendo sua dúvida sobre medicamentos. "
        "No entanto, qualquer orientação sobre medicação deve partir do seu médico responsável. "
        "Posso agendar uma teleconsulta para você tirar essas dúvidas diretamente com ele. "
        "Gostaria de agendar?"
    )
    nova_msg = {"role": "assistant", "content": resposta}
    return {**estado, "mensagens": [nova_msg], "resposta_final": resposta}


# --- NÓ: ESCALADA HUMANA ---
def no_escalada(estado: EstadoClinico) -> EstadoClinico:
    """Emite orientação de emergência imediata."""
    nova_msg = {"role": "assistant", "content": RESPOSTA_EMERGENCIA}
    return {**estado, "mensagens": [nova_msg], "resposta_final": RESPOSTA_EMERGENCIA, "escalada": True}


# --- NÓ: FORA DE ESCOPO ---
def no_fora_escopo(estado: EstadoClinico) -> EstadoClinico:
    """Responde que o assunto está fora do domínio."""
    nova_msg = {"role": "assistant", "content": RESPOSTA_FORA_ESCOPO}
    return {**estado, "mensagens": [nova_msg], "resposta_final": RESPOSTA_FORA_ESCOPO}


# --- ROTEAMENTO CONDICIONAL ---
def rotear(estado: EstadoClinico) -> str:
    intencao = estado.get("intencao", "triagem")
    mapa = {
        "escalada": "escalada",
        "prescricao": "prescricao",
        "fora_escopo": "fora_escopo",
        "triagem": "triagem"
    }
    return mapa.get(intencao, "triagem")


# --- MONTAGEM DO GRAFO ---
grafo = StateGraph(EstadoClinico)

grafo.add_node("supervisor", no_supervisor)
grafo.add_node("triagem", no_triagem)
grafo.add_node("prescricao", no_prescricao)
grafo.add_node("escalada", no_escalada)
grafo.add_node("fora_escopo", no_fora_escopo)

grafo.set_entry_point("supervisor")

grafo.add_conditional_edges(
    "supervisor",
    rotear,
    {
        "triagem": "triagem",
        "prescricao": "prescricao",
        "escalada": "escalada",
        "fora_escopo": "fora_escopo"
    }
)

grafo.add_edge("triagem", END)
grafo.add_edge("prescricao", END)
grafo.add_edge("escalada", END)
grafo.add_edge("fora_escopo", END)

app = grafo.compile()
print("✅ Grafo LangGraph compilado.")
print("   Nós: supervisor → [triagem | prescrição | escalada | fora_escopo]")