import json
import os
from collections import defaultdict
from evals.run_evals import executar_evals, EVAL_SET

def gerar_relatorio(resultados: list, tempos: list):
    print("\n" + "="*70)
    print("📊 RELATÓRIO DE EVALS — VitalBlua Sprint 2")
    print("="*70)

    total = len(resultados)
    adequadas  = sum(1 for r in resultados if r["avaliacao_qualitativa"] == "adequada")
    parciais   = sum(1 for r in resultados if r["avaliacao_qualitativa"] == "parcial")
    inadequadas = sum(1 for r in resultados if r["avaliacao_qualitativa"] == "inadequada")
    score_medio = round(sum(r["score"] for r in resultados) / total, 2)

    print(f"\n✅ Adequadas:   {adequadas}/{total}")
    print(f"⚠️  Parciais:    {parciais}/{total}")
    print(f"❌ Inadequadas: {inadequadas}/{total}")
    print(f"🎯 Score médio: {score_medio}/1.0")

    # Acurácia por categoria
    por_categoria = defaultdict(lambda: {"total": 0, "score": 0.0})
    for r in resultados:
        cat = r["categoria"]
        por_categoria[cat]["total"] += 1
        por_categoria[cat]["score"] += r["score"]

    print("\n📂 Score por Categoria:")
    for cat, dados in por_categoria.items():
        media = round(dados["score"] / dados["total"], 2)
        pct = int(media * 10)
        barra = "█" * pct + "░" * (10 - pct)
        print(f"   {cat:<15} [{barra}] {media}/1.0")

    # Taxa de escalada correta
    red_flags = [r for r in resultados if r["categoria"] == "red_flag"]
    if red_flags:
        corretas = sum(1 for r in red_flags if r["escalada_acionada"])
        print(f"\n🚨 Escalada correta (red_flag): {corretas}/{len(red_flags)}")

    # Tools mais acionadas
    todas_tools = []
    for r in resultados:
        todas_tools.extend([t["nome"] for t in r["tools_chamadas"]])
    if todas_tools:
        from collections import Counter
        contagem = Counter(todas_tools)
        print("\n🔧 Tools mais acionadas:")
        for tool, count in contagem.most_common():
            print(f"   {tool}: {count}x")

    # RAG
    com_rag = sum(1 for r in resultados if r["documentos_rag_recuperados"])
    print(f"\n📚 Casos com RAG acionado: {com_rag}/{total}")

    # Tempo
    print(f"\n⏱️  Tempo médio: {round(sum(tempos)/len(tempos), 2)}s")
    print(f"   Mínimo: {round(min(tempos), 2)}s | Máximo: {round(max(tempos), 2)}s")

    # Custo estimado
    tokens_por_interacao = 3000
    custo = round((tokens_por_interacao * 0.7 / 1e6 * 2.50) +
                  (tokens_por_interacao * 0.3 / 1e6 * 15.00), 5)
    print(f"\n💰 Custo estimado por conversa (GPT-5.4): ${custo} USD")
    print(f"   Modelo atual (Ollama local): $0.00")

    print("\n" + "="*70)


def exportar_resultados(resultados: list, caminho: str = "evals/sprint2_results.json"):
    """Exporta os resultados completos para JSON."""
    import os
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    payload = {
        "sprint": "Sprint 2",
        "modelo": "qwen3.5:9b via Ollama",
        "total_casos": len(resultados),
        "score_medio": round(sum(r["score"] for r in resultados) / len(resultados), 2),
        "resultados": resultados
    }

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"✅ Resultados exportados para {caminho}")


# Execução principal
if __name__ == "__main__":
    resultados_evals, tempos_evals = executar_evals(EVAL_SET)
    gerar_relatorio(resultados_evals, tempos_evals)
    exportar_resultados(resultados_evals)