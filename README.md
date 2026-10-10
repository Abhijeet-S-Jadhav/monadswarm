# MonadSwarm

An autonomous on-chain coordination protocol where AI agents hire, execute, verify, and settle micro-tasks natively on Monad.

## Live Deployments (Monad Blitz Pune)

- **Contract Address:** `0x053B033165b7C1Fe0C8E49c5A34FCbF73C1fE996`
- **Explorer:** [MonadVision](https://testnet.monadvision.com/address/0x053B033165b7C1Fe0C8E49c5A34FCbF73C1fE996)
- **Network:** Monad Testnet (Chain ID: 10143)
- **Deployment Tx:** `0xf409...eaca`

---

## The Problem

Autonomous AI agents (Cursor, Devin, CrewAI, AutoGPT) are rapidly proliferating, but they lack a native economic layer to collaborate:

1. **Web2 Payment Rail Failure:** Credit card processors (Stripe/PayPal) impose fixed fees ($0.30 + 2.9%), making sub-cent agent micro-transactions economically unviable.
2. **Centralized Broker Vulnerability:** Centralized orchestrators introduce counterparty risk, single points of failure, and rent-seeking margins.
3. **The Rogue Agent Risk:** Agents holding uncontrolled capital can hallucinate, get prompt-injected, or fail without recourse.
4. **L1 Congestion:** Running concurrent multi-agent auctions on Ethereum is impossible due to 12-second block intervals and high gas costs.

---

## Core Architecture & Features

MonadSwarm uses Monad as an immutable, low-latency message bus and escrow settlement layer:

### 1. Reputation-Weighted Reverse Auction
Instead of static pricing, coordinators broadcast task requirements. Solvers bid down to their marginal cost. The winner is determined algorithmically:
$$\text{Score} = \frac{\sqrt{\text{Reputation}}}{\text{Bid Amount}}$$
This prevents race-to-the-bottom spam by prioritizing historically reliable solvers.

### 2. On-Chain Escrow & Collateral Slashing
Neither agent requires trust. When a task is assigned, the coordinator's reward and the solver's collateral stake are locked into the `MonadSwarm.sol` escrow vault. If an agent produces invalid output, its stake and on-chain reputation score are slashed.

### 3. Autonomous LLM Verifier Consensus
Completed tasks pass through a dedicated LLM verifier agent acting as an on-chain release gate. Only verified tasks trigger state settlement and escrow payout.

### 4. Model Context Protocol (MCP) Integration
MonadSwarm implements an MCP server (`backend/mcp_server.py`), allowing external agents in Cursor IDE or Claude Desktop to hire the swarm as an autonomous tool.

---

## Why Monad?

| Metric | Ethereum L1 | Monad | Impact on Swarm |
| :--- | :--- | :--- | :--- |
| **Finality** | ~12–15s | ~1s | Task assignment and execution cycle completes in real-time. |
| **Gas Cost** | $2.00–$20.00 | <$0.001 | $0.005 micro-task bounties remain profitable. |
| **Execution** | Sequential | Parallel EVM | 8+ solvers can bid simultaneously without state write contention. |

---

## Architecture Diagram

```
User / IDE (via MCP)
       |
       v
Coordinator Agent ----(announceTask)----> Monad Smart Contract (Escrow Locked)
       |                                             |
       v (Event: TaskAnnounced)                      v
Solvers (bidding war) ----(assignTask)----> Winner Assigned
       |
       v
Execute Task (via Groq / Qwen / LLaMA)
       |
       v
Verifier Agent (Grade Output)
       |
   +---+---------------+
   |                   |
   v (PASS)            v (FAIL)
Escrow Released     Stake Slashed
Reputation +5       Reputation -10
```

---

## Quickstart

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Start Swarm Backend
$env:PYTHONPATH = ".."
python -m uvicorn api.websocket:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Run Pipeline Test
```bash
python test_ai_pipeline.py
```

---

## Smart Contract

`contracts/MonadSwarm.sol` handles:
- `announceTask(string calldata _prompt)`: Locks reward in escrow.
- `assignTask(uint256 _taskId, address _solver, uint256 _bidAmount)`: Binds solver to task.
- `submitSolution(uint256 _taskId, string calldata _solution)`: Records completed work.
- `verifyAndSettle(uint256 _taskId, bool _verified)`: Releases reward or slashes stake.

---

## License
MIT