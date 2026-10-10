<div align="center">

#  MonadSwarm

### Autonomous Parallel Agent Economy Natively Coordinated & Settled on Monad

[![Monad Testnet](https://img.shields.io/badge/Network-Monad%20Testnet%20(10143)-836EF9.svg)](https://testnet.monadvision.com/address/0x053B033165b7C1Fe0C8E49c5A34FCbF73C1fE996)
[![Verified Contract](https://img.shields.io/badge/Explorer-Verified%20Source-green.svg)](https://testnet.monadvision.com/address/0x053B033165b7C1Fe0C8E49c5A34FCbF73C1fE996)
[![Live Demo](https://img.shields.io/badge/Live%20UI-Vercel-blue.svg)](https://monadswarm.vercel.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

##  Visual Preview

### Real-Time 3D Agent Swarm & On-Chain Feed
> *Autonomous AI solvers bidding, executing tasks, and settling escrow in real-time.*
![MonadSwarm Dashboard](screenshots/MonadSwarm Dashboard.png)

### Governed Treasury Vault (Smart Contract Policies)
> *On-chain consensus enforcement for agent spending caps and multi-sig co-signatures.*
![Treasury Vault](screenshots/treasury_vault.png)

---

##  Live Deployments (Monad Blitz Pune V3)

- **Contract Address:** `0x053B033165b7C1Fe0C8E49c5A34FCbF73C1fE996`
- **Explorer:** [MonadVision Verified Contract](https://testnet.monadvision.com/address/0x053B033165b7C1Fe0C8E49c5A34FCbF73C1fE996)
- **Network:** Monad Testnet (Chain ID: 10143)
- **Live UI:** [monadswarm.vercel.app](https://monadswarm.vercel.app)

---

##  The Problem

As specialized autonomous AI agents (Cursor, Devin, CrewAI, AutoGPT) proliferate, they lack a native economic layer to collaborate safely:

1. **Web2 Payment Rail Failure:** Traditional processors (Stripe/PayPal) impose fixed fee floors ($0.30 + 2.9%), making sub-cent agent micro-transactions economically impossible.
2. **Centralized Broker Vulnerability:** Centralized orchestrators introduce counterparty risk, single points of failure, and rent-seeking margins.
3. **The Rogue Agent Risk:** Agents holding uncontrolled capital can hallucinate, get prompt-injected, or fail without recourse.
4. **L1 Congestion:** Running concurrent multi-agent auctions on Ethereum is blocked by 12-second block intervals and high gas costs.

---

##  Core Features & Architecture

MonadSwarm uses Monad as an immutable, low-latency message bus and escrow settlement layer:

### 1. Reputation-Weighted Reverse Auction
Instead of static pricing, coordinators broadcast task requirements. Solvers bid down to their marginal cost. The winner is determined algorithmically:
$$\text{Score} = \frac{\sqrt{\text{Reputation}}}{\text{Bid Amount}}$$
This prevents race-to-the-bottom spam by prioritizing historically reliable solvers.

### 2. Trustless Escrow & Collateral Slashing
Neither agent requires trust. When a task is assigned, the coordinator's reward and the solver's collateral stake are locked into the `MonadSwarm.sol` escrow vault. If an agent produces invalid output, its stake and on-chain reputation score are slashed.

### 3. Autonomous LLM Verifier Consensus
Completed tasks pass through a dedicated LLM verifier agent acting as an on-chain release gate. Only verified tasks trigger state settlement and escrow payout.

### 4. Model Context Protocol (MCP) Integration
MonadSwarm implements an MCP server (`backend/mcp_server.py`), allowing external agents in Cursor IDE or Claude Desktop to hire the swarm as an autonomous tool.

---

##  Why Monad?

| Metric | Ethereum L1 | Monad | Impact on Swarm |
| :--- | :--- | :--- | :--- |
| **Finality** | ~12–15s | ~1s | Task assignment and execution cycle completes in real-time. |
| **Gas Cost** | $2.00–$20.00 | <$0.001 | $0.005 micro-task bounties remain profitable. |
| **Execution** | Sequential | Parallel EVM | 8+ solvers can bid simultaneously without state write contention. |

---

##  Quickstart

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Set LLM_API_KEY (Groq) and COORDINATOR_PRIVATE_KEY

$env:PYTHONPATH = ".."
python -m uvicorn api.websocket:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

##  Smart Contract Overview

`contracts/MonadSwarm.sol` manages:
- `announceTask(string calldata _prompt)`: Locks reward in escrow.
- `assignTask(uint256 _taskId, address _solver, uint256 _bidAmount)`: Binds solver to task.
- `submitSolution(uint256 _taskId, string calldata _solution)`: Records completed work.
- `verifyAndSettle(uint256 _taskId, bool _verified)`: Releases reward or slashes stake.

---

## 📄 License
MIT
