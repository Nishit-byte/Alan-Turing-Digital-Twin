from app.retrieval.embedder import Embedder
from app.retrieval.vector_store import VectorStore
from app.retrieval.reranker import Reranker
from app.config import settings

class Retriever:
    def __init__(self):
        self.embedder = Embedder(settings.embedding_model)
        self.store = VectorStore(settings.chroma_db_path)
        self.reranker = Reranker()

    def get_ranked_chunks(self, query: str, initial_k: int = 10, final_k: int = 5) -> list[dict]:
        """
        Retrieve initial_k chunks via cosine similarity, then rerank
        with a cross-encoder and return top final_k with confidence scores.
        """
        query_embedding = self.embedder.embed_query(query)
        results = self.store.query(query_embedding, n_results=initial_k)
        raw_chunks = results["documents"][0] if results["documents"] else []

        if not raw_chunks:
            return []

        reranked = self.reranker.rerank(query, raw_chunks)
        return reranked[:final_k]

    def get_context_string(self, query: str, n_results: int = 5) -> str:
        """Legacy plain-text context (kept for backward compatibility)."""
        ranked = self.get_ranked_chunks(query, initial_k=10, final_k=n_results)
        return "\n\n---\n\n".join(r["text"] for r in ranked)