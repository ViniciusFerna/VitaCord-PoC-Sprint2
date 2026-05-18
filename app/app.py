import streamlit as st
from src.graph.chat import chat
from evals.run_evals import executar_evals, EVAL_SET
from evals.gerar_rel_evals import gerar_relatorio, exportar_resultados

st.set_page_config(page_title="VitalBlua", page_icon="🩺")
st.title("🩺 VitalBlua — Assistente de Saúde")

# Sidebar com evals
st.sidebar.title("🧪 Evals")
if st.sidebar.button("Executar Suite de Evals"):
    with st.spinner("Executando evals..."):
        resultados_evals, tempos_evals = executar_evals(EVAL_SET)
        exportar_resultados(resultados_evals)
    gerar_relatorio(resultados_evals, tempos_evals)
    st.sidebar.success("✅ Resultados salvos em evals/sprint2_results.json")

# Inicializa o histórico na sessão do Streamlit
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Exibe o histórico de mensagens
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Campo de input
if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processando..."):
            resultado = chat(prompt, historico=st.session_state.mensagens)

        st.markdown(resultado["resposta"])
        st.caption(f"Intenção: `{resultado['intencao']}` | Tempo: `{resultado['tempo']}s`")

        if resultado["escalada"]:
            st.error("🚨 Escalada de emergência acionada")

        # Trajetória de agentes
        if resultado["trace"]["agentes_acionados"]:
            trajetoria = " → ".join(resultado["trace"]["agentes_acionados"])
            st.caption(f"🗺️ Trajetória: `{trajetoria}`")

        # Documentos RAG recuperados
        if resultado["trace"]["documentos_rag"]:
            with st.expander(f"📚 RAG — {len(resultado['trace']['documentos_rag'])} documento(s) recuperado(s)"):
                for i, doc in enumerate(resultado["trace"]["documentos_rag"], 1):
                    st.markdown(f"**Documento {i}**")
                    st.text(doc)
                    st.divider()

        # Tools chamadas
        if resultado["trace"]["tools_chamadas"]:
            with st.expander(f"🔧 Tools — {len(resultado['trace']['tools_chamadas'])} chamada(s)"):
                for tool in resultado["trace"]["tools_chamadas"]:
                    st.markdown(f"**`{tool['nome']}`**")
                    st.json(tool["argumentos"])
                    st.divider()

    st.session_state.mensagens.append({
        "role": "assistant",
        "content": resultado["resposta"]
    })