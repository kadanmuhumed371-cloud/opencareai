from abc import ABC, abstractmethod
import os
from google import genai
from google.genai import types

class TranslationService(ABC):
    @abstractmethod
    def translate_medical_text(self, text: str, source_language: str, target_language: str) -> str:
        pass

class GeminiTranslationService(TranslationService):
    def __init__(self):
        # We can reuse the API key from environment
        api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyBRaPCwOynVH3916Bhxc6X5Ga7ng5lEKXY").strip()
        self.client = genai.Client(api_key=api_key)
        
    def translate_medical_text(self, text: str, source_language: str, target_language: str) -> str:
        prompt = f"""
        You are a professional medical translator.
        Translate the following medical text from {source_language} to {target_language}.
        Preserve the medical meaning while using language that ordinary people can understand.
        Never invent or modify medical information during translation.
        
        Text to translate:
        "{text}"
        """
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerationConfig(temperature=0.1)
            )
            return response.text.strip() if response.text else "Translation failed."
        except Exception as e:
            return f"Translation error: {str(e)}"

class MockTranslationService(TranslationService):
    def translate_medical_text(self, text: str, source_language: str, target_language: str) -> str:
        return f"[Mock Translation from {source_language} to {target_language}]: {text}"

def get_translation_service() -> TranslationService:
    # return MockTranslationService() # Un-comment to use mock
    return GeminiTranslationService()
