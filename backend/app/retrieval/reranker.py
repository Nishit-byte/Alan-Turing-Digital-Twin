from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, chunks: list[str]) -> list[dict]:
        """
        Score each chunk's relevance to the query using a cross-encoder.
        Returns chunks sorted by relevance with normalized confidence scores (0-1).
        """
        if not chunks:
            return []

        pairs = [(query, chunk) for chunk in chunks]
        raw_scores = self.model.predict(pairs)

        # normalize scores to 0-1 range using sigmoid-like scaling
        min_score, max_score = min(raw_scores), max(raw_scores)
        score_range = max_score - min_score if max_score != min_score else 1

        results = [
            {
                "text": chunk,
                "raw_score": float(score),
                "confidence": float((score - min_score) / score_range)
            }
            for chunk, score in zip(chunks, raw_scores)
        ]

        return sorted(results, key=lambda x: x["raw_score"], reverse=True)