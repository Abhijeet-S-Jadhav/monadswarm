import os
import httpx
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("LLM_API_KEY", "")

headers = {"Authorization": f"Bearer {key}"}
res = httpx.get("https://api.groq.com/openai/v1/models", headers=headers)

if res.status_code == 200:
    print("ALL AVAILABLE MODELS:")
    for m in res.json().get("data", []):
        print("- " + m.get("id", ""))
else:
    print("Error:", res.text)
