from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat_routes import router as chat_router
from app.api.session_routes import router as session_router

app = FastAPI(title="Alan Turing Digital Twin")
allow_origins=["alan-turing-digital-twin-4es0h7gcw-nishitgoel4-3248s-projects.vercel.app", "http://localhost:5173"],
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(session_router)

@app.get("/health")
def health():
    return {"status": "ok"}