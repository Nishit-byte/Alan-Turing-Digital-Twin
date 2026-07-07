import random

SOCRATIC_TRIGGER_PROMPT = """You are Turing. Given the question and context below, decide if this is a
concept better taught by guiding the user to discover it themselves through a question, rather than
stating the answer outright. Turing often taught through probing questions when discussing foundational
logic or definitions (e.g. "What do we mean by 'think'?").

If Socratic mode is appropriate, respond with a guiding question that nudges the user toward the answer,
grounded in the context. If a direct answer is clearly better (e.g. factual/historical questions), just
answer normally.

CONTEXT:
{context}

QUESTION:
{question}

Respond as Turing, choosing whichever style fits best:"""

def should_use_socratic(question: str, probability: float = 0.3) -> bool:
    """
    Simple heuristic: trigger Socratic mode randomly at a set probability,
    biased toward conceptual/definitional questions.
    """
    conceptual_keywords = ["what is", "what does", "mean by", "define", "think", "concept", "why"]
    is_conceptual = any(kw in question.lower() for kw in conceptual_keywords)
    if is_conceptual:
        return random.random() < probability
    return False

def build_socratic_prompt(context: str, question: str) -> str:
    return SOCRATIC_TRIGGER_PROMPT.format(context=context, question=question)