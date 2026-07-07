import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.gemini_api_key)

class GeminiClient:
    def __init__(self, model_name: str = "gemini-2.5-flash-lite"):
        self.model = genai.GenerativeModel(model_name)

    def generate(self, prompt: str) -> str:
        """Send a prompt to Gemini and return the text response."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"[Error generating response: {e}]"