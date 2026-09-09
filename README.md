# AGY Quantitative Trading System

An institutional-grade, Event-Driven Architecture (EDA) quantitative trading system designed for extreme scalability, low latency, and absolute state sovereignty.

## Architecture Highlights
* **Zero-Block EventBus**: Built on asynchronous pub/sub principles to bypass Python GIL limitations during high-frequency tick bursts.
* **Dual-Engine Backtesting**: Decouples Vectorized parameter sweeps from Event-Driven live simulation (achieving 100% code symmetry between backtest and live).
* **Risk Sovereignty**: The Risk Engine (C16) sits as a mandatory, isolated gateway. It maintains its own parallel ledger via WebSocket fills and active REST reconciliation, completely untrusting strategy-level accounting.

## Documentation
* [Research & Strategy Matrix](docs/research/strategy-taxonomy-matrix.md)
* [Technical Implementation Blueprint](docs/research/technical-implementation-blueprint.md)
* [System Premortem & Danger Zones](docs/architecture/system_premortem.md)
* [Market Data Pipeline](docs/architecture/market_data_pipeline.md)
* [Risk Engine Specs](docs/architecture/risk_engine.md)

## Quick Start
```bash
pip install -r requirements.txt
python main.py
```
