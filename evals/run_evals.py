import json
from src.graph.chat import chat

# Carrega o eval set do JSON
with open("evals/eval_set.json", "r", encoding="utf-8") as f:
    EVAL_SET = json.load(f)

def avaliar_qualitativamente(caso: dict, resultado: dict) -> tuple[str, float]:
    """
    Avalia a resposta em três níveis: adequada, parcial ou inadequada.
    Retorna (avaliacao_str, score_numerico).

    Score:
      1.0 = adequada   — todos os critérios atendidos
      0.5 = parcial    — critérios positivos atendidos mas falhou em algum negativo
      0.0 = inadequada — falhou em critério crítico
    """
    resposta = resultado["resposta"].lower()
    erros_criticos = []
    erros_parciais = []

    # Verifica intenção esperada
    if "esperado_intencao" in caso:
        if resultado["intencao"] != caso["esperado_intencao"]:
            erros_criticos.append(
                f"intenção incorreta: esperado '{caso['esperado_intencao']}', "
                f"obtido '{resultado['intencao']}'"
            )

    # Verifica escalada esperada
    if "esperado_escalada" in caso:
        if resultado["escalada"] != caso["esperado_escalada"]:
            erros_criticos.append(
                f"escalada incorreta: esperado {caso['esperado_escalada']}, "
                f"obtido {resultado['escalada']}"
            )

    # Verifica termos obrigatórios
    for termo in caso.get("deve_conter", []):
        if termo.lower() not in resposta:
            erros_parciais.append(f"ausente: '{termo}'")

    # Verifica termos proibidos
    for termo in caso.get("nao_deve_conter", []):
        if termo.lower() in resposta:
            erros_criticos.append(f"contém termo proibido: '{termo}'")

    if erros_criticos:
        return "inadequada", 0.0, erros_criticos + erros_parciais
    elif erros_parciais:
        return "parcial", 0.5, erros_parciais
    else:
        return "adequada", 1.0, []


def executar_evals(eval_set: list, verbose: bool = False) -> list:
    """
    Executa a suite de evals e retorna lista de resultados detalhados
    para exportação em /evals/sprint2_results.json.
    """
    resultados_json = []
    tempos = []

    print("\n🧪 Executando suite de evals...\n")
    print("-" * 70)

    for caso in eval_set:

        resultado = chat(caso["entrada"], verbose=verbose)
        tempos.append(resultado["tempo"])

        avaliacao, score, erros = avaliar_qualitativamente(caso, resultado)

        status = {"adequada": "✅", "parcial": "⚠️", "inadequada": "❌"}[avaliacao]
        print(f"{status} [{caso['id']}] {caso['categoria']} — {caso['entrada'][:55]}...")
        if erros:
            for e in erros:
                print(f"       → {e}")

        # Monta o registro completo para o JSON de resultados
        registro = {
            "id": caso["id"],
            "categoria": caso["categoria"],
            "pergunta": caso["entrada"],
            "resposta_obtida": resultado["resposta"],
            "trajetoria_agentes": resultado["trace"]["agentes_acionados"],
            "tools_chamadas": resultado["trace"]["tools_chamadas"],
            "documentos_rag_recuperados": resultado["trace"]["documentos_rag"],
            "avaliacao_qualitativa": avaliacao,
            "score": score,
            "erros_identificados": erros,
            "intencao_detectada": resultado["intencao"],
            "escalada_acionada": resultado["escalada"],
            "tempo_resposta_segundos": resultado["tempo"]
        }

        resultados_json.append(registro)

    return resultados_json, tempos


