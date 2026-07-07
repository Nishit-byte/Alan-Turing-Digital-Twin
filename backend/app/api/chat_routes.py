from fastapi import APIRouter
from pydantic import BaseModel
from app.retrieval.retriever import Retriever
from app.core.prompt_templates import build_prompt
from app.core.reasoning_trace import build_reasoning_trace
from app.core.socratic_mode import should_use_socratic, build_socratic_prompt
from app.llm.gemini_client import GeminiClient
from app.memory.short_term import short_term_memory
from app.memory.long_term import long_term_memory

router = APIRouter()

retriever = Retriever()
gemini = GeminiClient()

class ChatRequest(BaseModel):
    session_id: str
    question: str

class ReasoningStep(BaseModel):
    step: int
    source_excerpt: str
    confidence: float
    raw_score: float

class ChatResponse(BaseModel):
    answer: str
    context_used: str
    reasoning_trace: list[ReasoningStep]
    overall_confidence: float
    socratic_mode: bool

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id
    question = request.question

    ranked_chunks = retriever.get_ranked_chunks(question, initial_k=10, final_k=5)
    context = "\n\n---\n\n".join(c["text"] for c in ranked_chunks)

    recent_history = short_term_memory.get_history_string(session_id)
    past_summary = long_term_memory.get_past_summaries(session_id)

    use_socratic = should_use_socratic(question)

    if use_socratic:
        prompt = build_socratic_prompt(context, question)
    else:
        prompt = build_prompt(context, question, recent_history, past_summary)

    answer = gemini.generate(prompt)

    short_term_memory.add_turn(session_id, "user", question)
    short_term_memory.add_turn(session_id, "assistant", answer)
    long_term_memory.save_turn(session_id, "user", question)
    long_term_memory.save_turn(session_id, "assistant", answer)

    turn_count = short_term_memory.turn_count(session_id)
    long_term_memory.save_summary_if_needed(session_id, recent_history, turn_count)

    trace = build_reasoning_trace(ranked_chunks, question)

    return ChatResponse(
        answer=answer,
        context_used=context,
        reasoning_trace=trace["steps"],
        overall_confidence=trace["overall_confidence"],
        socratic_mode=use_socratic
    )