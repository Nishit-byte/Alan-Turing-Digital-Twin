# Alan Turing — Digital Twin

A RAG-powered conversational AI grounded in Alan Turing's own writings — his 1936 and 1950 papers, and biographical material — using retrieval-augmented generation, two-tier memory, and reasoning transparency to hold grounded, in-character conversations.

Built as a differentiated take on "digital twin" chatbots: instead of just answering questions, it shows *how* it arrived at each answer (retrieval confidence, reasoning trace) and sometimes teaches Socratically, the way Turing himself often did.

## Demo

*(Add a screenshot or GIF of the chat UI here once you have one — this is the single highest-impact thing you can add to this README)*

## Features

- **RAG pipeline** grounded in Turing's actual papers ("On Computable Numbers," "Computing Machinery and Intelligence") — not general LLM knowledge
- **Cross-encoder reranking** with per-chunk confidence scores, surfaced via a reasoning trace panel
- **Two-tier memory**: short-term in-session buffer + SQLite-backed long-term memory with Gemini-distilled session summaries
- **Socratic mode**: on conceptual questions, sometimes responds with a guiding question rather than a direct answer, mirroring Turing's actual teaching style
- **Session history**: past conversations are listed, resumable, and deletable
- **Custom neon UI** with animated gradient wisps and circuit-trace motifs

## Architecture
PDF/text sources
│
▼
[Chunker] → RecursiveCharacterTextSplitter (~500 tokens)
│
▼
[Embedder] → SentenceTransformer (all-MiniLM-L6-v2)
│
▼
[ChromaDB] ← persisted vector store
│
▼ (on query)
[Retriever] → cosine similarity top-10
│
▼
[Reranker] → cross-encoder, confidence-scored top-5
│
▼
[Prompt Builder] → injects context + short/long-term memory
│
▼
[Gemini] → persona-grounded response
│
▼
[Memory] → short-term buffer + SQLite long-term + summarization
│
▼
FastAPI → React frontend

## Tech stack

| Layer | Technology |
|---|---|
| Embeddings | SentenceTransformers (`all-MiniLM-L6-v2`) |
| Reranking | Cross-encoder (`ms-marco-MiniLM-L-6-v2`) |
| Vector store | ChromaDB |
| LLM | Google Gemini API |
| Memory | SQLite + SQLAlchemy |
| Backend | FastAPI |
| Frontend | React + Vite |

## Setup

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

Create `backend/.env` (see `.env.example`) and add your [Gemini API key](https://aistudio.google.com/apikey):

Ingest the source documents (already included in `data/raw/`):
```bash
python scripts/ingest_documents.py
```

Run the server:
```bash
python -m uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` (backend must be running on `http://127.0.0.1:8000`).

## Source material

All source documents are public domain — Turing's UK copyright expired 70 years after his 1954 death:
- *On Computable Numbers, with an Application to the Entscheidungsproblem* (1936)
- *Computing Machinery and Intelligence*, Mind (1950)
- Biographical material

## Author

Built by [Nishit](https://github.com/Nishit-byte) as an AI/ML portfolio project.

