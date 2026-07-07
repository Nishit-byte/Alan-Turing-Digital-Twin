from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from app.config import settings

Base = declarative_base()

class SessionSummary(Base):
    __tablename__ = "session_summaries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, index=True)
    summary_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class ConversationTurn(Base):
    __tablename__ = "conversation_turns"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, index=True)
    role = Column(String)          # "user" or "assistant"
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_engine(f"sqlite:///{settings.data_processed_path}/../turing.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)