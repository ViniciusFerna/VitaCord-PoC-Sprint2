import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from data.knowledge_base.documentos import DOCUMENTOS_CLINICOS

# Inicializa o cliente ChromaDB em memória
chroma_client = chromadb.Client()

# Função de embedding usando nomic-embed-text via Ollama (local)
embedding_fn = OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name="nomic-embed-text"
)

# Cria a coleção (vector store)
colecao = chroma_client.get_or_create_collection(
    name="base_clinica_careplus",
    embedding_function=embedding_fn
)

# Indexa os documentos
colecao.add(
    documents=[doc["conteudo"] for doc in DOCUMENTOS_CLINICOS],
    ids=[doc["id"] for doc in DOCUMENTOS_CLINICOS]
)

print(f"✅ Base de conhecimento indexada com {colecao.count()} documentos.")


def recuperar_contexto(query: str, n_resultados: int = 2) -> str:
    """Busca os documentos mais relevantes para a query no vector store."""
    resultados = colecao.query(
        query_texts=[query],
        n_results=n_resultados
    )
    documentos = resultados["documents"][0]
    return "\n\n---\n\n".join(documentos)


# Teste rápido do RAG
print("\n🔍 Teste do RAG — query: 'dor no peito e falta de ar'")
print("-" * 50)
contexto = recuperar_contexto("dor no peito e falta de ar")
print(contexto[:300] + "...")