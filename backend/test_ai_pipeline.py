import asyncio
import httpx
import time

API_BASE = "http://localhost:8000"

async def test_ai_swarm():
    print("=" * 60)
    print("?? TESTING REAL AI TASK INJECTION INTO MONADSWARM")
    print("=" * 60)

    prompt = "Explain in two sentences how Monad's parallel execution improves throughput over Ethereum."

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Post the AI Task to the running Coordinator
        print(f"\n?? 1. Posting AI Task: '{prompt}'")
        res = await client.post(
            f"{API_BASE}/api/control/create-task",
            params={
                "reward": 50000000,
                "task_type": "ai_task",
                "prompt": prompt,
                "source": "terminal_test"
            }
        )
        data = res.json()
        task_id = data.get("task_id")
        print(f"? Task Created on Swarm! Task ID: {task_id}")

        # 2. Poll until the solver bids, solves via LLM, and gets verified
        print("\n? 2. Swarm bidding and solving in progress (calling Groq LLaMA-3.1)...")
        for _ in range(20):
            await asyncio.sleep(2)
            stats = (await client.get(f"{API_BASE}/stats")).json()
            history = stats.get("task_history", [])
            task = next((t for t in history if t.get("task_id") == task_id), None)

            if task:
                status = task.get("status")
                print(f"   Current status: {status}")
                if status in ("completed", "rejected", "failed"):
                    print("\n" + "=" * 60)
                    print(f"?? TASK FINALIZED! Status: {status.upper()}")
                    print(f"?? Winning Solver: {task.get('assigned_to')}")
                    print(f"?? Winning Bid: {task.get('bid_amount')} sompi/wei")
                    print("\n?? LLM OUTPUT PRODUCED:")
                    print("-" * 60)
                    print(task.get("solution"))
                    print("-" * 60)
                    return

    print("?? Test timed out waiting for task completion.")

if __name__ == "__main__":
    asyncio.run(test_ai_swarm())
