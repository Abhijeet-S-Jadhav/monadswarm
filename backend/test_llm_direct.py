import asyncio
import os
from dotenv import load_dotenv

# Force load .env
load_dotenv()

from backend.llm_client import get_llm

async def main():
    print("=" * 60)
    print("?? DIAGNOSING LLM CLIENT CONFIGURATION")
    print("=" * 60)
    
    key = os.getenv("LLM_API_KEY", "")
    base_url = os.getenv("LLM_BASE_URL", "")
    model = os.getenv("LLM_MODEL", "")
    
    print(f"Base URL: {base_url}")
    print(f"Model:    {model}")
    print(f"API Key:  {'Configured (' + key[:8] + '...)' if key and key != 'your_groq_key_here' else '? MISSING OR DEFAULT PLACEHOLDER'}")
    
    llm = get_llm()
    print(f"\nLLM Client is_available(): {llm.is_available()}")
    
    if not llm.is_available():
        print("\n?? Problem Found: API key is not set in backend/.env!")
        return

    print("\n?? Attempting test completion call to Groq...")
    response = await llm.complete(
        system="You are a helpful assistant.",
        user="Say 'Groq connection successful!' in 3 words.",
        max_tokens=20
    )
    print(f"\n?? Direct Response from Groq: {response}")

if __name__ == "__main__":
    asyncio.run(main())
