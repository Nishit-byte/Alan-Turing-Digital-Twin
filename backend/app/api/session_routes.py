from fastapi import APIRouter
from app.memory.long_term import long_term_memory
from app.memory.short_term import short_term_memory

router = APIRouter()

@router.get("/sessions")
def list_sessions():
    return long_term_memory.list_sessions()

@router.get("/sessions/{session_id}/messages")
def get_session_messages(session_id: str):
    return long_term_memory.get_session_messages(session_id)

@router.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    long_term_memory.delete_session(session_id)
    short_term_memory.clear_session(session_id)
    return {"status": "deleted", "session_id": session_id}