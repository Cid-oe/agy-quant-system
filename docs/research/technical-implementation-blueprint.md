# Technical Implementation Blueprint
**Classification:** Chief Architect Synthesis  
**Input Sources:** research-strategy.md · strategy-taxonomy-matrix.md · repository-ranking-scores.md · build-queue-analysis.md · comprehensive-crypto-quant-report.md

---

## SECTION 0 — Cross-File Consistency Audit

### 0.1 Confirmed Consistencies
The five documents are broadly internally consistent on the following invariants:

| Invariant | Confirmed in |
|---|---|
| Freqtrade = top Python retail engine | ranking, report, taxonomy |
| Hummingbot = top for market making | ranking, report, taxonomy |
| NautilusTrader = top for HFT/institutional | ranking, report, build-queue |
| CCXT = universal exchange API layer | report, taxonomy, build-queue |
| VectorBT = fastest vectorized backtesting, no live execution | ranking, build-queue, taxonomy |
| Qlib+RD-Agent = ML alpha research, no live execution | ranking, report, build-queue |
| Standalone risk proxy = #1 build priority | build-queue, report |
| Basis/funding rate = highest evidence systematic edge | taxonomy (Grade A), report (Edge #1) |
| RL = sim-to-real gap, not safe live | taxonomy (Grade C), ranking (C+), report |
| LLM agentic = experimental, not safe live | taxonomy (Grade D), ranking (C/D+) |

### 0.2 Contradictions Detected

| ID | Contradiction | Files in Conflict | Resolution |
|---|---|---|---|
| **C-01** | **RL Grade Mismatch.** taxonomy-matrix grades RL as "C — massive sim-to-real gap." ranking-scores grades FinRL as "C+." A plus-modifier implies marginal viability not conveyed in the taxonomy. | taxonomy vs ranking | Adopt C (no plus). FinRL-X is a distinct sub-component; grade it separately as C+ when paired with a live execution wrapper. |
| **C-02** | **VectorBT→NautilusTrader Adapter is Priority 3** in build-queue but is **never mentioned** in the comprehensive-report's Strategic Action Plan (which lists only 4 steps and skips this component). | build-queue vs report | Adapter must be inserted as Step 3a in the implementation order. Its omission from the report is a synthesis error. |
| **C-03** | **Mean Reversion is classed under Cat. 4 ("Statistical Arbitrage" sub-type)** in the taxonomy but given its own Category (Cat. 4 Mean Reversion). The sub-type list for Cat. 4 includes "Statistical Arbitrage" — conflating two distinct categories (5 and 4). | taxonomy (Cat. 4 vs Cat. 5) | Mean Reversion (Cat. 4) = single-asset reversion. Statistical Arbitrage (Cat. 5) = cross-asset spread. Sub-type label in Cat. 4 must be corrected to "Cointegration-based reversion" not "Statistical Arbitrage." |
| **C-04** | **OpenAlice Evidence Discrepancy.** ranking gives OpenAlice Score "C" with a warning it is "explicitly beta." taxonomy places LLM/Agentic systems (Cat. 13) at Evidence Grade "D." These are numerically inconsistent: C ≠ D. | ranking vs taxonomy | OpenAlice receives a split grade: **C for UI/workflow architecture; D for live execution safety**. The taxonomy's D is correct for the execution dimension. |
| **C-05** | **No unified backtester gap** is identified in build-queue (Gap B) as unsolved, but the research-strategy (M20) lists ABIDES and Qlib as backtesting tools — implying they partially address on-chain/CEX hybrid simulation. This claim in build-queue is **partially unsupported**. | build-queue vs research-strategy | Gap B is real but overstated. Qlib + event-driven simulation covers ~70% of CEX side. True gap is the EVM mempool ingestion layer. Scope the missing tool accordingly. |

### 0.3 Duplicated Recommendations

| ID | Duplicate | Appears in |
|---|---|---|
| **D-01** | "Build Standalone Risk Proxy" | build-queue Priority 1 AND report Section F Step 2 — identical recommendation stated twice with different names ("Risk & Policy Proxy" vs "Universal Risk Proxy") |
| **D-02** | "Deploy Freqtrade + FreqAI" | report Section F Step 1 AND implied by taxonomy Cat. 11 + ranking 1.1 verdict |
| **D-03** | "Automate Basis/Funding Rate Trading" | build-queue Priority 2 AND report Section F Step 3 AND taxonomy Cat. 6 (Grade A) — appears in all three documents |
| **D-04** | "VectorBT for research, NautilusTrader for live" | build-queue Priority 3 AND report Section F Step 4 — same recommendation, different framing |

**Deduplication decision:** Merge all four into a single canonical build pipeline (see Section 4).

### 0.4 Unsupported Claims

| ID | Claim | Source | Issue |
|---|---|---|---|
| **U-01** | "Over 80% of retail trading bots fail in live production" | comprehensive-report Section D | No citation. Negative-evidence report (SA-16) gave "73–95%" range — use that range with source attribution. |
| **U-02** | Basis trading is "highest conviction, lowest-risk systematic edge" | build-queue Priority 2 | Requires caveat: funding rates can turn negative (funding rate flips in bear markets). Not unconditionally low risk. Add condition: "when funding is persistently positive (>0.01% per 8h)." |
| **U-03** | "RD-Agent automates the entire R&D lifecycle" | report Section C | RD-Agent is experimental. The claim implies production maturity not established in any source document. Downgrade to "automates alpha factor *hypothesis* generation." |
| **U-04** | Volatility & Options rated Evidence Grade "A — Highly profitable" | taxonomy Cat. 7 | No specific crypto options strategy or repository received Grade A validation in any sub-report. Options market making requires Deribit institutional access and specialized Greeks modeling. Downgrade to B+. |
| **U-05** | "NautilusTrader is rapidly becoming the standard for open-source institutional deployments" | report Section A | No institutional adoption data cited. Infrastructure report (SA-18) confirms architectural merit but cites no production institutional users. Change to "architected for institutional deployments." |

---

## SECTION 1 — Top 25 Reusable Components

Derived from cross-referencing all five documents. Each component is categorized by layer and tagged with the primary source tools that implement or provide it.

| # | Component | Layer | Primary Implementation | Reuse Scope |
|---|---|---|---|---|
| C01 | **Exchange Connectivity Abstraction** | Execution | CCXT (REST), CCXT Pro (WebSocket) | All execution bots |
| C02 | **Order State Machine** | Execution | NautilusTrader OrderBook, Hummingbot OMS | Market making, arb, HFT |
| C03 | **WebSocket Feed Normalizer** | Data Ingestion | Cryptofeed, barter-data (Rust) | All real-time strategies |
| C04 | **OHLCV Candle Store** | Data Storage | ArcticDB, DuckDB+Parquet | All research and ML |
| C05 | **Tick/LOB Store** | Data Storage | ClickHouse, QuestDB | HFT, microstructure, arb |
| C06 | **Feature Engineering Pipeline** | ML | Qlib DataHandler, FreqAI feature pipeline, pandas-ta | All ML strategies |
| C07 | **Vectorized Backtest Engine** | Research | VectorBT (Pro) | All strategy prototyping |
| C08 | **Event-Driven Backtest Engine** | Research | NautilusTrader BacktestEngine, Lean | HFT, market making |
| C09 | **Walk-Forward Optimizer** | Research | Freqtrade Hyperopt, VectorBT walk-forward | All validated strategies |
| C10 | **Gradient Boosted Tree Model** | ML Alpha | XGBoost / LightGBM (via Qlib) | ML prediction, factor models |
| C11 | **Time-Series Transformer** | ML Alpha | TFT, PatchTST, iTransformer (via Qlib/Darts) | Price/volume forecasting |
| C12 | **Orderbook Imbalance Signal** | Signal | DeepLOB architecture, HftBacktest L2 data | Microstructure alpha |
| C13 | **Funding Rate Monitor** | Signal | CoinGlass API, Binance Futures /fapi | Basis/carry strategies |
| C14 | **On-Chain Flow Ingestion** | Data Ingestion | DefiLlama API, Dune Analytics, CoinMetrics | Macro regime, on-chain alpha |
| C15 | **Sentiment & NLP Signal** | Signal | CryptoPanic, GDELT, ElKulako/CryptoBERT | News shock, liquidation |
| C16 | **Risk & Policy Proxy** | Risk | Custom Rust proxy (to build) | ALL strategies — universal |
| C17 | **Kelly / Position Sizer** | Risk | PyPortfolioOpt, custom Kelly implementation | All strategies |
| C18 | **Regime Detector** | Signal | VectorBT + macro features, Qlib regime model | Hybrid/multi-strategy routing |
| C19 | **Liquidation Cascade Detector** | Signal | CoinGlass Liquidation Heatmap API | Liquidation/event-driven |
| C20 | **Delta-Neutral Hedger** | Execution | Custom CCXT scripts (to productionize) | Basis trading |
| C21 | **Prometheus + Grafana Monitor** | Observability | Standard OSS stack | All live deployments |
| C22 | **Docker Compose Deployment Unit** | Infrastructure | Freqtrade Docker, Hummingbot Docker | All containerized strategies |
| C23 | **CI/CD Canary Pipeline** | Infrastructure | GitHub Actions + paper-trading gate | All production updates |
| C24 | **ML Model Registry** | MLOps | MLflow / W&B | All ML-driven strategies |
| C25 | **ML→Execution Inference Gateway** | Bridge | Apache Arrow/Flight (to build) | ML-to-live bridge |

---

## SECTION 2 — Dependency Graph

```
LAYER 0: Raw Market Data
│
├── [C03] WebSocket Feed Normalizer ──────────────────────────┐
│    └── exchange WebSocket streams (via C01 CCXT Pro)        │
│                                                             ▼
├── [C04] OHLCV Candle Store (DuckDB/ArcticDB) ◄─────── Batch pulls (C01 REST)
│
└── [C05] Tick/LOB Store (ClickHouse/QuestDB) ◄──────── C03 normalized ticks

LAYER 1: Signal Generation
│
├── [C06] Feature Engineering Pipeline
│    ├── inputs: C04, C05, C13, C14, C15
│    └── outputs: feature tensors → C10, C11
│
├── [C10] Gradient Boosted Tree (XGBoost/LightGBM)
│    └── inputs: C06 features
│
├── [C11] Time-Series Transformer (TFT/PatchTST)
│    └── inputs: C06 features
│
├── [C12] Orderbook Imbalance Signal
│    └── inputs: C05 Tick/LOB Store (real-time)
│
├── [C13] Funding Rate Monitor
│    └── inputs: CoinGlass API, Binance fapi (direct)
│
├── [C14] On-Chain Flow Ingestion
│    └── inputs: DefiLlama, Dune (batched)
│
├── [C15] Sentiment/NLP Signal
│    └── inputs: CryptoPanic, GDELT
│
└── [C18] Regime Detector
     └── inputs: C06, C13, C14 (macro + microstructure fusion)

LAYER 2: Research & Validation
│
├── [C07] Vectorized Backtest (VectorBT)
│    └── inputs: C04, C06 features → used for parameter sweep
│
├── [C08] Event-Driven Backtest (NautilusTrader)
│    └── inputs: C05 (tick-level), C06 features → production validation
│
├── [C09] Walk-Forward Optimizer
│    └── wraps: C07 or C08
│
└── [C24] ML Model Registry (MLflow/W&B)
     └── stores: C10, C11 model versions → promotes to C25

LAYER 3: Execution
│
├── [C02] Order State Machine
│    ├── inputs: signals from C10/C11/C12/C13/C15/C18
│    ├── routes through: C16 Risk & Policy Proxy (MANDATORY)
│    └── executes via: C01 CCXT / NautilusTrader gateway
│
├── [C20] Delta-Neutral Hedger
│    ├── inputs: C13 Funding Rate Monitor
│    └── routes through: C16 Risk & Policy Proxy
│
└── [C25] ML→Execution Inference Gateway (Arrow/Flight)
     ├── inputs: C10/C11 live inference
     └── outputs: structured signals → C02 Order State Machine

LAYER 4: Risk & Control (Cross-cutting)
│
└── [C16] Risk & Policy Proxy ← WRAPS ALL LAYER 3 OUTPUTS
     ├── enforces: max drawdown, exposure limits, fat-finger
     └── kill switch: disconnects C01 on breach

LAYER 5: Observability
│
├── [C21] Prometheus + Grafana Monitor
│    └── scrapes: C02, C16, C20, C25 metrics
│
├── [C22] Docker Compose Deployment
│    └── wraps: entire stack per strategy
│
└── [C23] CI/CD Canary Pipeline
     └── gates: C07→C08→paper-trade→canary→production

LAYER 6: MLOps
│
├── [C24] ML Model Registry
│    └── version-controls: C10, C11 artifacts
│
└── [C06] Feature Pipeline (retraining DAG via Airflow/Prefect)
```

---

## SECTION 3 — Component Graph (Grouped by System)

```
┌─────────────────────────────────────────────────────────────────────┐
│  SYSTEM A: DATA FABRIC                                              │
│  C01 ─► C03 ─► C05 (Tick/LOB)                                      │
│  C01 ─► C04 (OHLCV Candle)                                         │
│  C14 (On-Chain) ─► C06                                             │
│  C13 (Funding) ─► C18, C20                                         │
│  C15 (Sentiment) ─► C18, C02                                       │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│  SYSTEM B: ALPHA RESEARCH                                           │
│  C04+C05 ─► C06 ─► C10 (GBDT) ─► C24 (Registry)                   │
│             C06 ─► C11 (Transformer) ─► C24                        │
│  C05 ─► C12 (LOB Imbalance)                                        │
│  C04+C05 ─► C07 (VectorBT) ─► C09 (Walk-Forward) ─► C08 (Nautilus)│
│  C24 ─► C25 (Inference Gateway)                                     │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│  SYSTEM C: EXECUTION                                                │
│  C25+C12+C18 ─► C02 (Order State Machine) ─► C16 ─► C01           │
│  C13 ─► C20 (Delta-Neutral Hedger) ─► C16 ─► C01                  │
│  C16 = MANDATORY GATEWAY (no order bypasses)                        │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│  SYSTEM D: INFRASTRUCTURE & OBSERVABILITY                           │
│  C22 (Docker) ─► wraps all systems                                  │
│  C23 (CI/CD) ─► gates all deployments                              │
│  C21 (Grafana) ─► monitors all live systems                        │
│  C24 (MLflow) ─► governs all model versions                        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## SECTION 4 — Implementation Order

Canonical build sequence after deduplication of D-01 through D-04 and correction of contradiction C-02.

### Phase 0 — Infrastructure Bedrock (Weeks 1–3)
| Step | Component | Action | Tooling |
|---|---|---|---|
| 0.1 | C22 | Docker Compose scaffold for all services | Docker, docker-compose |
| 0.2 | C01 | CCXT connector pool (async, WebSocket + REST) | ccxt, ccxt.pro |
| 0.3 | C21 | Prometheus + Grafana monitoring baseline | Prometheus, Grafana, Loki |
| 0.4 | C23 | CI/CD pipeline: lint → unit test → paper-trade gate → canary | GitHub Actions |

### Phase 1 — Data Fabric (Weeks 3–6)
| Step | Component | Action | Tooling |
|---|---|---|---|
| 1.1 | C03 | WebSocket feed normalizer (tick + LOB) | Cryptofeed or barter-data |
| 1.2 | C04 | OHLCV candle store | DuckDB + Parquet on S3 |
| 1.3 | C05 | Tick/LOB store | QuestDB (dev) → ClickHouse (scale) |
| 1.4 | C13 | Funding rate monitor | CoinGlass API + Binance fapi |
| 1.5 | C14 | On-chain ingestion daemon | DefiLlama API + Dune client |
| 1.6 | C15 | Sentiment feed parser | CryptoPanic API + CryptoBERT |

### Phase 2 — Risk Proxy (Weeks 5–7, Overlaps Phase 1)
| Step | Component | Action | Tooling |
|---|---|---|---|
| 2.1 | **C16** | **Build standalone Rust Risk & Policy Proxy** | Rust + Axum/Tokio |
| 2.2 | C16 | Integrate: max drawdown halt, fat-finger filter, exposure cap | Custom |
| 2.3 | C16 | Expose metrics endpoint → C21 | Prometheus client |
| 2.4 | C16 | Integration tests against exchange simulators | Paper trade / mock exchange |

> **NOTE:** C16 MUST be deployed before any live order is routed. No exceptions.

### Phase 3 — First Live Strategy: Basis Trading (Weeks 7–10)
| Step | Component | Action | Tooling |
|---|---|---|---|
| 3.1 | C20 | Delta-neutral hedger — spot leg + perp short | Custom CCXT |
| 3.2 | C13→C20 | Wire funding rate monitor → hedger trigger | Internal event bus |
| 3.3 | C17 | Kelly position sizer — conservative fraction | PyPortfolioOpt |
| 3.4 | C16→C20 | Route ALL orders through risk proxy | C16 |
| 3.5 | C21 | Dashboard: PnL, net delta, funding accrual | Grafana |

### Phase 4 — Research Stack (Weeks 8–13)
| Step | Component | Action | Tooling |
|---|---|---|---|
| 4.1 | C06 | Feature engineering pipeline (v1: OHLCV + funding + on-chain) | pandas-ta + Qlib DataHandler |
| 4.2 | C07 | VectorBT parameter sweeps on top strategy ideas | VectorBT |
| 4.3 | C09 | Walk-forward optimizer wrapper | Freqtrade Hyperopt / custom |
| 4.4 | C08 | Event-driven backtest (NautilusTrader) for top-3 sweep winners | NautilusTrader |
| 4.5 | C10 | XGBoost/LightGBM alpha model v1 | Qlib + XGBoost |
| 4.6 | C24 | ML model registry — log all experiments | MLflow |

### Phase 5 — ML→Execution Bridge (Weeks 13–17)
| Step | Component | Action | Tooling |
|---|---|---|---|
| 5.1 | C11 | Train TFT / PatchTST transformer model | PyTorch + Qlib |
| 5.2 | C25 | Build ML→Execution Inference Gateway | Apache Arrow/Flight |
| 5.3 | C24→C25 | Promote champion model from registry to gateway | MLflow → Arrow server |
| 5.4 | C02 | Extend Order State Machine to consume C25 signals | NautilusTrader actor |
| 5.5 | C18 | Regime detector: gate ML signals by regime | Qlib regime model |

### Phase 6 — Microstructure Strategy (Weeks 16–21)
| Step | Component | Action | Tooling |
|---|---|---|---|
| 6.1 | C05 | Upgrade ClickHouse for real-time LOB queries | ClickHouse |
| 6.2 | C12 | LOB imbalance signal (DeepLOB CNN or OFI metric) | PyTorch / numpy |
| 6.3 | C08 | HFT backtest on LOB imbalance using HftBacktest | HftBacktest |
| 6.4 | C02 | Sub-second order routing (NautilusTrader Rust actor) | NautilusTrader |
| 6.5 | C16 | Upgrade risk proxy latency profile for HFT gate | Rust async |

### Phase 7 — AutoML & Automated Alpha Discovery (Weeks 20+)
| Step | Component | Action | Tooling |
|---|---|---|---|
| 7.1 | C06 | Automated feature factory (RD-Agent) | Qlib + RD-Agent |
| 7.2 | C10+C11 | Ensemble: GBDT + Transformer signal blending | Custom |
| 7.3 | C18 | Advanced regime switching: macro + microstructure fusion | Qlib + custom |
| 7.4 | C25 | Multi-model inference gateway (A/B model serving) | Arrow Flight + MLflow |

---

## SECTION 5 — Implementation Difficulty Estimates

| Component | Difficulty | Rationale |
|---|---|---|
| C01 — CCXT connector | ★★☆☆☆ | Well-documented, massive community |
| C03 — Feed normalizer | ★★★☆☆ | WebSocket reconnect logic, sequence tracking |
| C04 — OHLCV store | ★☆☆☆☆ | DuckDB is trivial; Parquet layout needs schema discipline |
| C05 — Tick/LOB store | ★★★★☆ | ClickHouse schema for LOB deltas is non-trivial at scale |
| C06 — Feature pipeline | ★★★☆☆ | Feature leakage prevention requires extreme care |
| C07 — VectorBT | ★★☆☆☆ | Easy API, but Numba cold-start debugging is painful |
| C08 — Event-driven BT | ★★★★☆ | NautilusTrader actor model is complex |
| C09 — Walk-forward optimizer | ★★★☆☆ | Correct temporal splits are deceptively hard |
| C10 — GBDT model | ★★☆☆☆ | Mature tooling; risk is feature engineering quality |
| C11 — Transformer model | ★★★★☆ | Attention mask design for financial sequences is specialized |
| C12 — LOB imbalance | ★★★★☆ | Requires tick-perfect data alignment |
| C13 — Funding monitor | ★★☆☆☆ | Simple API polling with rate-limit handling |
| C14 — On-chain ingestion | ★★★☆☆ | API rate limits + reorg handling |
| C15 — Sentiment/NLP | ★★★☆☆ | Model selection + timestamp alignment |
| **C16 — Risk proxy** | **★★★★★** | **Mission-critical; must be provably correct under concurrent load** |
| C17 — Kelly sizer | ★★☆☆☆ | Math is well-defined; parameter estimation is the hard part |
| C18 — Regime detector | ★★★★☆ | Non-stationarity makes regime labels inherently noisy |
| C19 — Liquidation detector | ★★★☆☆ | CoinGlass API + real-time cascade classification |
| C20 — Delta-neutral hedger | ★★★☆☆ | Legging risk on simultaneous spot+perp execution |
| C21 — Grafana monitoring | ★★☆☆☆ | Standard infrastructure; metric design requires thought |
| C22 — Docker Compose | ★★☆☆☆ | Straightforward; network_mode: host for HFT |
| C23 — CI/CD canary | ★★★☆☆ | Paper-trading gate logic requires mock exchange |
| C24 — ML model registry | ★★☆☆☆ | MLflow setup is trivial; governance policy is not |
| **C25 — ML→Exec gateway** | **★★★★★** | **Zero-copy inference across language boundaries is novel engineering** |

---

## SECTION 6 — Resolved Build Sequence (Canonical, Deduplicated)

```
Phase 0 [Infra Bedrock]:    C22 → C01 → C21 → C23
Phase 1 [Data Fabric]:      C03 → C04 → C05 → C13 → C14 → C15
Phase 2 [Risk Proxy]:       C16  ← BUILD AND HARDEN BEFORE ANY LIVE ORDER
Phase 3 [First Strategy]:   C13+C17+C20 → routed through C16
Phase 4 [Research Stack]:   C06 → C07 → C09 → C08 → C10 → C24
Phase 5 [ML↔Exec Bridge]:   C11 → C25 → C02 extended → C18
Phase 6 [HFT Layer]:        C12 → upgraded C08 → C02 Rust actor → C16 HFT profile
Phase 7 [AutoML]:           C06 (RD-Agent) → C10+C11 ensemble → C18 advanced → C25 A/B
```

**Single-line dependency chain:**  
`[C01,C03] → [C04,C05] → [C06,C13,C14,C15] → C16 → [C07,C09,C08,C10,C20,C24] → [C11,C17,C18,C19] → C25 → C02 → (live strategies)`

---

## SECTION 7 — Critical Path & Risk Flags

| Flag | Description | Mitigation |
|---|---|---|
| 🔴 | **C16 (Risk Proxy) is the single highest-risk component.** No live order should bypass it. A bug here loses real money. | Formal spec + property-based testing (proptest). Separate security review before any capital exposure. |
| 🔴 | **C25 (ML→Exec Gateway) introduces undefined latency.** Arrow Flight serialization adds ~1–5ms. Unacceptable for HFT; acceptable for swing/basis. | Profile before wiring to microstructure strategies (C12). Use dedicated HFT signal path (C12→C02 direct) bypassing C25. |
| 🟡 | **Feature leakage (C06) is the #1 ML failure mode.** Any global normalization before train/test split corrupts all downstream models. | Enforce strict temporal train/test splits at feature pipeline level. Log split boundaries in C24. |
| 🟡 | **Funding rate polarity risk (C20).** Funding rates invert during bear markets, turning basis trades into directional bets. | C13 must expose 30-day rolling funding sign; C16 must halt C20 if sign flips negative. |
| 🟢 | **Basis trading (C20) is the safest entry point.** Delta-neutral, free data, straightforward execution, validated Grade A. | Start here. Prove C16 in production at small scale before wiring C25. |
