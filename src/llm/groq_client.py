from langchain_core.language_models.llms import LLM
from typing import Optional, List
from groq import Groq
from pydantic import PrivateAttr
from src.config import Config


class GroqLLM(LLM):
    _client: Groq = PrivateAttr()

    model_name: str = Config.GROQ_MODEL
    temperature: float = 0.2
    max_tokens: int = 2048

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        key = Config.GROQ_API_KEY
        if not key:
            raise RuntimeError("GROQ_API_KEY not found in environment")

        self._client = Groq(api_key=key)

    @property
    def _llm_type(self) -> str:
        return "groq"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self._client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a strict JSON and tool calling agent."},
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        return response.choices[0].message.content
    
def get_llm():
    return GroqLLM()