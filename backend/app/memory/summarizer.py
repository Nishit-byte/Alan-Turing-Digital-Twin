from app.llm.gemini_client import GeminiClient

SUMMARY_PROMPT = """Summarize the following conversation between a user and Turing (a digital twin)
in 3-5 concise sentences. Focus on what topics were discussed and any important context
that would help continue this conversation later. Do not include pleasantries.

CONVERSATION:
{conversation}

SUMMARY:"""

class Summarizer:
    def __init__(self):
        self.gemini = GeminiClient()

    def summarize(self, conversation_text: str) -> str:
        prompt = SUMMARY_PROMPT.format(conversation=conversation_text)
        return self.gemini.generate(prompt)