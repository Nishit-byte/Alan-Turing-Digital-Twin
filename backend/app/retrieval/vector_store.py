import chromadb
from chromadb.config import Settings as ChromaSettings

class VectorStore:
    def __init__(self, persist_path: str, collection_name: str = "turing_docs"):
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_chunks(self, chunks: list[dict], embeddings: list[list[float]]):
        """Add chunks + their embeddings to the vector store."""
        self.collection.add(
            ids=[c["chunk_id"] for c in chunks],
            embeddings=embeddings,
            documents=[c["text"] for c in chunks],
            metadatas=[{"source": c["source"]} for c in chunks]
        )

    def query(self, query_embedding: list[float], n_results: int = 5) -> dict:
        """Query the vector store for nearest chunks."""
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

    def count(self) -> int:
        return self.collection.count()