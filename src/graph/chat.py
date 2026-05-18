import time
from src.graph.graph import app


def chat(mensagem_usuario: str, historico: list = None, paciente_id: str = "P001", verbose: bool = True) -> dict:
    """
    Processa uma mensagem pelo grafo completo.
    Retorna dict com resposta, intenção, tempo, escalada e rastreamento completo.
    """
    historico = historico or []  # DEVE ser a primeira linha
    historico.append({"role": "user", "content": mensagem_usuario})

    

    # Versão instrumentada do grafo para capturar a trajetória
    estado_inicial = {
        "mensagens": list(historico),
        "paciente_id": paciente_id,
        "contexto_rag": "",
        "intencao": "",
        "resposta_final": "",
        "escalada": False,
        "tools_chamadas": []
    }

    inicio = time.time()
    resultado =  app.invoke(estado_inicial)

    # Rastreamento da execução
    trace = {
        "agentes_acionados": [],
        "tools_chamadas": resultado.get("tools_chamadas", []),
        "documentos_rag": []
    }

    # Intercepta os nós do grafo para rastrear trajetória
    for evento in app.stream(estado_inicial):
        for no, estado in evento.items():
            trace["agentes_acionados"].append(no)

            # Captura documentos RAG se disponíveis
            if estado.get("contexto_rag"):
                docs = [
                    d.strip()[:100] + "..."
                    for d in estado["contexto_rag"].split("---")
                    if d.strip()
                ]
                trace["documentos_rag"] = docs

            # Captura tools chamadas a partir do histórico de mensagens
            for msg in estado.get("mensagens", []):
                if isinstance(msg, dict) and msg.get("role") == "tool":
                    # Recupera o nome da tool a partir da mensagem anterior
                    pass

            estado_final = estado

    tempo = round(time.time() - inicio, 2)

    # Captura tools a partir do histórico de mensagens do estado final
    for msg in estado_final.get("mensagens", []):
        if isinstance(msg, dict):
            tool_calls = msg.get("tool_calls", [])
            for tc in tool_calls:
                nome = tc.get("function", {}).get("name", "")
                args = tc.get("function", {}).get("arguments", {})
                if nome:
                    trace["tools_chamadas"].append({
                        "nome": nome,
                        "argumentos": args
                    })

    resposta = estado_final.get("resposta_final", "")
    historico.append({"role": "assistant", "content": resposta})

    if verbose:
        print(f"\n{'='*60}")
        print(f"👤 Usuário: {mensagem_usuario}")
        print(f"🔀 Intenção: {estado_final.get('intencao', '')}")
        print(f"🗺️  Trajetória: {' → '.join(trace['agentes_acionados'])}")
        if trace["tools_chamadas"]:
            print(f"🔧 Tools: {[t['nome'] for t in trace['tools_chamadas']]}")
        if trace["documentos_rag"]:
            print(f"📚 RAG: {len(trace['documentos_rag'])} documento(s) recuperado(s)")
        print(f"⏱️  Tempo: {tempo}s")
        print(f"{'='*60}")
        print(f"🤖 Agente: {resposta}")

    return {
        "resposta": resposta,
        "intencao": estado_final.get("intencao", ""),
        "escalada": estado_final.get("escalada", False),
        "tempo": tempo,
        "trace": trace
    }


print("✅ Função de chat com rastreamento configurada.")