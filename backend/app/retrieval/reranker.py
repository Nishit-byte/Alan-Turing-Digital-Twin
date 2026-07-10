from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            self._model = CrossEncoder(self.model_name)
        return self._model

    def rerank(self, query: str, chunks: list[str]) -> list[dict]:
        if not chunks:
            return []
        pairs = [(query, chunk) for chunk in chunks]
        raw_scores = self.model.predict(pairs)
        min_score, max_score = min(raw_scores), max(raw_scores)
        score_range = max_score - min_score if max_score != min_score else 1
        results = [
            {"text": chunk, "raw_score": float(score), "confidence": float((score - min_score) / score_range)}
            for chunk, score in zip(chunks, raw_scores)
        ]
        return sorted(results, key=lambda x: x["raw_score"], reverse=True)