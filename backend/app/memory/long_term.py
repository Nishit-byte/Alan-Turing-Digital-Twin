from app.memory.models import SessionLocal, SessionSummary, ConversationTurn
from app.memory.summarizer import Summarizer
from sqlalchemy import func

class LongTermMemory:
    def __init__(self):
        self.summarizer = Summarizer()

    def save_turn(self, session_id: str, role: str, content: str):
        db = SessionLocal()
        try:
            turn = ConversationTurn(session_id=session_id, role=role, content=content)
            db.add(turn)
            db.commit()
        finally:
            db.close()

    def save_summary_if_needed(self, session_id: str, history_string: str, turn_count: int, threshold: int = 12):
        if turn_count >= threshold:
            summary_text = self.summarizer.summarize(history_string)
            db = SessionLocal()
            try:
                summary = SessionSummary(session_id=session_id, summary_text=summary_text)
                db.add(summary)
                db.commit()
            finally:
                db.close()

    def get_past_summaries(self, session_id: str) -> str:
        db = SessionLocal()
        try:
            summaries = (
                db.query(SessionSummary)
                .filter(SessionSummary.session_id == session_id)
                .order_by(SessionSummary.created_at.asc())
                .all()
            )
            return "\n".join(s.summary_text for s in summaries)
        finally:
            db.close()

    def list_sessions(self) -> list[dict]:
        """Return one row per session: id, first user message (as title), last activity time."""
        db = SessionLocal()
        try:
            session_ids = db.query(ConversationTurn.session_id).distinct().all()
            sessions = []
            for (sid,) in session_ids:
                first_turn = (
                    db.query(ConversationTurn)
                    .filter(ConversationTurn.session_id == sid, ConversationTurn.role == "user")
                    .order_by(ConversationTurn.created_at.asc())
                    .first()
                )
                last_turn = (
                    db.query(ConversationTurn)
                    .filter(ConversationTurn.session_id == sid)
                    .order_by(ConversationTurn.created_at.desc())
                    .first()
                )
                if first_turn and last_turn:
                    sessions.append({
                        "session_id": sid,
                        "title": first_turn.content[:60],
                        "last_activity": last_turn.created_at.isoformat()
                    })
            return sorted(sessions, key=lambda s: s["last_activity"], reverse=True)
        finally:
            db.close()

    def get_session_messages(self, session_id: str) -> list[dict]:
        db = SessionLocal()
        try:
            turns = (
                db.query(ConversationTurn)
                .filter(ConversationTurn.session_id == session_id)
                .order_by(ConversationTurn.created_at.asc())
                .all()
            )
            return [{"role": t.role, "content": t.content} for t in turns]
        finally:
            db.close()

    def delete_session(self, session_id: str):
        db = SessionLocal()
        try:
            db.query(ConversationTurn).filter(ConversationTurn.session_id == session_id).delete()
            db.query(SessionSummary).filter(SessionSummary.session_id == session_id).delete()
            db.commit()
        finally:
            db.close()
            
long_term_memory = LongTermMemory()