import sys
from pathlib import Path

# allow importing from app/ when running this script directly
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.retrieval.chunker import process_document
from app.retrieval.embedder import Embedder
from app.retrieval.vector_store import VectorStore

def ingest_all_documents():
    raw_dir = Path(settings.data_raw_path)
    files = list(raw_dir.glob("*.pdf")) + list(raw_dir.glob("*.txt"))

    if not files:
        print(f"No documents found in {raw_dir}. Add PDFs/txt files there first.")
        return

    print(f"Found {len(files)} document(s) to ingest.")

    embedder = Embedder(settings.embedding_model)
    store = VectorStore(settings.chroma_db_path)

    for file_path in files:
        print(f"\nProcessing: {file_path.name}")
        chunks = process_document(str(file_path), settings.chunk_size, settings.chunk_overlap)
        print(f"  -> {len(chunks)} chunks created")

        texts = [c["text"] for c in chunks]
        embeddings = embedder.embed_texts(texts)

        store.add_chunks(chunks, embeddings)
        print(f"  -> Added to ChromaDB")

    print(f"\nDone. Total chunks in store: {store.count()}")

if __name__ == "__main__":
    ingest_all_documents()