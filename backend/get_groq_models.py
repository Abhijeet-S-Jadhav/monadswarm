import os
import httpx
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("LLM_API_KEY", "")

headers = {"Authorization": f"Bearer {key}"}
res = httpx.get("https://api.groq.com/openai/v1/models", headers=headers)

if res.status_code == 200:
    print("ACTIVE GROQ MODELS:")
    for m in res.json().get("data", []):
        mid = m.get("id", "")
        if "llama" in mid or "mixtral" in mid or "gemma" in mid:
            print("- " + mid)
else:
    print("Error:", res.text)
