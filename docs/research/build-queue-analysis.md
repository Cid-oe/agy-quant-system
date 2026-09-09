# Gap Analysis & Build Queue (M31)

This document identifies the missing infrastructural and strategic components in the current open-source quantitative crypto trading ecosystem, and prioritizes a build queue based on expected value, reproducibility, and capital efficiency.

## 1. Identified Ecosystem Gaps

### A. The "Sim-to-Real" Chasm in Machine Learning
*   **The Gap:** There are excellent ML research platforms (Qlib) and excellent execution engines (NautilusTrader, Freqtrade), but the bridge between them is heavily fragmented. Transitioning a PyTorch model into a low-latency C++/Rust execution pipeline requires bespoke, proprietary engineering.
*   **Missing Tool:** A standardized, zero-copy inference gateway that links Python-trained ML models directly into Rust execution memory spaces without serialization overhead (e.g., using Apache Arrow/Flight).

### B. Lack of Standardized On-Chain / CEX Hybrid Backtesters
*   **The Gap:** Backtesting CEX order books is solved (VectorBT, HftBacktest). Backtesting on-chain DeFi swaps is semi-solved (Dune SQL, local fork testing). But there is no unified backtester that can perfectly simulate a cross-venue arbitrage (e.g., Binance Spot vs. Uniswap V3) accounting for Ethereum block times, gas spikes, and CEX API latency simultaneously.
*   **Missing Tool:** A unified event-driven simulator that ingests both CEX WebSocket feeds and EVM mempool state changes synchronously.

### C. Open-Source Risk & Policy Engines
*   **The Gap:** Open-source bots package risk management *inside* the strategy logic. Institutional setups decouple this. If a strategy goes rogue, the separate policy engine kills the connection.
*   **Missing Tool:** A standalone, low-latency Risk Gateway (Policy Engine) proxy. All orders from any bot (Freqtrade, Hummingbot, Custom) route through this proxy, which enforces hard exposure limits, drawdown halts, and fat-finger checks before hitting the exchange API.

### D. Automated Funding Rate Arbitrage Tooling
*   **The Gap:** Spot-perpetual basis trading is highly profitable and low risk, but currently requires custom scripts to monitor cross-exchange funding rates and execute delta-neutral legs simultaneously without legging risk.
*   **Missing Tool:** An open-source, dedicated Delta-Neutral Yield Management platform that automates cash-and-carry trades across top exchanges with integrated margin monitoring.

---

## 2. Prioritized Build Queue

Ranking Formula: `Expected Research Value × Reproducibility × Data Availability × Capital Efficiency ÷ Risk`

### Priority 1: The Standalone Risk & Policy Proxy
*   **Concept:** A lightweight Rust proxy server that sits between algorithmic strategies and exchange APIs (e.g., wrapping CCXT calls).
*   **Why:** Immediately applicable to *any* existing bot. Reduces the risk of catastrophic account blowups (the #1 cause of failure) to near zero.
*   **Capital Efficiency:** High (Protects capital).

### Priority 2: Spot-Perpetual Basis Engine
*   **Concept:** A dedicated execution bot for harvesting funding rates.
*   **Why:** It is the highest conviction, lowest-risk systematic edge in crypto. Data is freely available (CoinGlass, Binance Futures), and execution is straightforward but requires precise simultaneous execution.
*   **Capital Efficiency:** Very High (Delta-neutral).

### Priority 3: VectorBT to NautilusTrader Adapter
*   **Concept:** An open-source translation layer that takes a strategy optimized in VectorBT (Python) and compiles it into a deployable NautilusTrader (Rust) node.
*   **Why:** Bridges the gap between the fastest research tool and the fastest execution tool, solving the deployment bottleneck for quant researchers.
*   **Capital Efficiency:** Medium.

### Priority 4: LLM-Assisted Feature Engineering Pipeline
*   **Concept:** An automated pipeline that uses LLMs (like Claude or GPT-4) to read financial papers, extract the mathematical formulas for alpha factors, and automatically write the Python/Pandas code to generate those features for Qlib.
*   **Why:** Dramatically accelerates alpha discovery, turning unstructured academic text into structured trading signals.
*   **Capital Efficiency:** Low (Research focused).
