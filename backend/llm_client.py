import os
from typing import Optional
import httpx
from dotenv import load_dotenv

# Force load .env from the backend directory
load_dotenv()

class LLMClient:
    def __init__(self):
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1").rstrip("/")
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.model = os.getenv("LLM_MODEL", "qwen/qwen3.8-27b")
        self._client: Optional[httpx.AsyncClient] = None
        print(f"🤖 LLM Client Initialized | Model: {self.model} | Available: {self.is_available()}")

    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key != "your_groq_key_here")

    def _http(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=60.0)
        return self._client

    async def complete(self, system: str, user: str, max_tokens: int = 512,
                       temperature: float = 0.3) -> Optional[str]:
        if not self.is_available():
            print("⚠️ LLM call skipped: API key not available")
            return None
        try:
            resp = await self._http().post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
            )
            if resp.status_code != 200:
                print(f"⚠️ LLM call failed: HTTP {resp.status_code} {resp.text[:200]}")
                return None
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"⚠️ LLM call error: {e}")
            return None

    async def close(self):
        if self._client is not None:
            await self._client.aclose()
            self._client = None

_llm: Optional[LLMClient] = None

def get_llm() -> LLMClient:
    global _llm
    if _llm is None:
        _llm = LLMClient()
    return _llm
