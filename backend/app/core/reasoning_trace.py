def build_reasoning_trace(ranked_chunks: list[dict], question: str) -> dict:
    """
    Structures retrieved chunks into a reasoning trace object:
    what was retrieved, how confident, and in what order they were considered.
    """
    return {
        "question": question,
        "steps": [
            {
                "step": i + 1,
                "source_excerpt": chunk["text"][:200] + ("..." if len(chunk["text"]) > 200 else ""),
                "confidence": round(chunk["confidence"], 3),
                "raw_score": round(chunk["raw_score"], 3)
            }
            for i, chunk in enumerate(ranked_chunks)
        ],
        "overall_confidence": round(
            sum(c["confidence"] for c in ranked_chunks) / len(ranked_chunks), 3
        ) if ranked_chunks else 0.0
    }