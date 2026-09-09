# Quantitative Trading Repositories: Ranking & Scoring (M30)

This document scores and ranks the top quantitative crypto trading frameworks discovered during the research phases based on their production readiness, evidence of success, and overall architecture.

## Evidence Grading Scale
*   **A**: Production-ready, robust live trading support, institutional-grade architecture.
*   **B**: High potential, strong out-of-sample/backtest evidence, but requires significant engineering to deploy safely.
*   **C**: Plausible research tools, excellent for prototyping, but lack native, reliable live execution infrastructure.
*   **D**: Educational, academic, or highly experimental. Severe "sim-to-real" gap. Not safe for live capital without complete overhauls.

---

## 1. Execution & Backtesting Frameworks

### 1.1. Freqtrade
*   **Score: A**
*   **Strengths:** Best-in-class documentation, seamless Docker installation, massive community, integrated FreqAI (Machine Learning), robust dry-run and live CCXT integration.
*   **Weaknesses:** Python event loop can struggle with ultra-high frequency (microsecond) trading.
*   **Verdict:** The absolute gold standard for retail to mid-tier quantitative crypto trading.

### 1.2. Hummingbot
*   **Score: A-**
*   **Strengths:** Industry standard for market making and arbitrage (CEX and DEX). Strong connectivity, institutional backing.
*   **Weaknesses:** Rapidly changing exchange connectors can introduce breaking bugs; memory leak issues in sustained high-throughput environments.
*   **Verdict:** Essential for liquidity provision and arbitrage strategies.

### 1.3. NautilusTrader
*   **Score: B+**
*   **Strengths:** Rust-native core, ultra-low latency, deterministic execution, unified backtest and live execution code paths.
*   **Weaknesses:** Steep learning curve, requires heavy engineering and Rust knowledge for advanced deployments.
*   **Verdict:** The premier open-source choice for serious institutional HFT and latency-sensitive deployments.

### 1.4. QuantConnect Lean
*   **Score: B+**
*   **Strengths:** Massive institutional C# framework, incredibly detailed modeling of corporate actions, fees, and slippage.
*   **Weaknesses:** Heavyweight, overkill for simple crypto setups, primarily oriented towards traditional finance (equities/options) with crypto bolted on.
*   **Verdict:** Excellent for cross-asset portfolios (Crypto + Equities).

### 1.5. VectorBT (and VectorBT PRO)
*   **Score: B**
*   **Strengths:** Unmatched speed for vectorized parameter sweeps and exploratory data analysis (EDA).
*   **Weaknesses:** Vectorized backtests ignore path dependency and order queue dynamics. Live execution is non-native.
*   **Verdict:** Mandatory for rapid strategy prototyping and parameter optimization, but must be paired with an event-driven engine for live deployment.

---

## 2. Machine Learning & Research Platforms

### 2.1. Microsoft Qlib (with RD-Agent)
*   **Score: B+ (For Research)**
*   **Strengths:** Unparalleled for AI-driven factor mining and portfolio optimization. RD-Agent automates alpha discovery.
*   **Weaknesses:** Zero live execution capabilities. It is purely an offline research and modeling platform.
*   **Verdict:** Best-in-class for generating ML-based alpha, requires a separate execution layer (like NautilusTrader or CCXT).

### 2.2. FinRL (and FinRL-X)
*   **Score: C+**
*   **Strengths:** Great educational environments (Gym) for applying Reinforcement Learning to trading.
*   **Weaknesses:** Base repo is highly academic with massive sim-to-real gaps. Installation dependency hell.
*   **Verdict:** Transition to FinRL-X for production. Highly experimental edge.

---

## 3. Microstructure & Order Book Simulators

### 3.1. HftBacktest
*   **Score: B-**
*   **Strengths:** Highly specialized for tick-by-tick order book queue simulation. Accurate latency modeling.
*   **Weaknesses:** Experimental live trading features, limited exchange support natively.
*   **Verdict:** The best open-source tool for researching latency arbitrage and LOB imbalances before writing a proprietary Rust execution engine.

### 3.2. DeepLOB
*   **Score: D (For Live Trading), A (For Academic Research)**
*   **Strengths:** Foundational architecture for applying deep CNNs to limit order books.
*   **Weaknesses:** No execution framework. Purely Jupyter notebooks and PyTorch scripts.
*   **Verdict:** Provides the neural network blueprint, but zero plumbing.

---

## 4. Agentic & LLM Systems

### 4.1. OpenAlice
*   **Score: C**
*   **Strengths:** Innovative UI and "Trading-as-Git" concept for LLM orchestration.
*   **Weaknesses:** Execution is explicitly marked as beta and dangerous. 
*   **Verdict:** A bleeding-edge workspace for experimenting with LLM agents, not for live capital.

### 4.2. ai-hedge-fund (virattt)
*   **Score: D+**
*   **Strengths:** Excellent demonstration of multi-agent debate and reasoning.
*   **Weaknesses:** No execution, no risk management layers.
*   **Verdict:** Purely educational/simulation.
