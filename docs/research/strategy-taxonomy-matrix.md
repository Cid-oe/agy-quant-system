# Strategy Matrix & Taxonomy (M29)

This matrix classifies the discovered quantitative crypto trading ecosystems, frameworks, and strategies into 16 distinct categories based on their operational mechanism.

## 1. Arbitrage (Cross-Exchange / Spatial)
Exploiting price discrepancies for the same asset across different exchanges (CEX-CEX) or between Centralized and Decentralized exchanges (CEX-DEX).
- **Core Repositories**: Blackbird (Historical benchmark), Hummingbot (Standard for CEX/DEX Arb), CCXT (Infrastructure layer).
- **Sub-Types**: Triangular arbitrage, Atomic Arbitrage, Latency Arbitrage.
- **Evidence Grade**: B (Viable but highly competitive, requires significant infrastructure and capital).

## 2. Market Making (Liquidity Provision)
Providing liquidity to both sides of the order book to capture the bid-ask spread while managing inventory risk.
- **Core Repositories**: Hummingbot, Tribeca (Avellaneda-Stoikov model), Caladan (Educational).
- **Sub-Types**: Avellaneda-Stoikov inventory models, AMM concentrated liquidity provisioning (Uniswap v3).
- **Evidence Grade**: A (Profitable for those with institutional infrastructure, fee tiers, and low latency).

## 3. Momentum / Trend Following
Capturing sustained directional price movements based on historical momentum indicators.
- **Core Repositories**: Freqtrade, Zenbot, PyAlgoTrade, Backtesting.py.
- **Sub-Types**: Moving Average Crossovers, Breakout Strategies, Time-Series Momentum.
- **Evidence Grade**: C (Prone to whipsaws in choppy markets, negative expectancy on lower timeframes without strong filters).

## 4. Mean Reversion
Betting that prices will return to a historical average or fair value after an extreme deviation.
- **Core Repositories**: Freqtrade, VectorBT.
- **Sub-Types**: Bollinger Band reversals, RSI divergence, Statistical Arbitrage.
- **Evidence Grade**: B- (Viable on short intraday horizons due to negative autocorrelation in crypto, but carries tail risk).

## 5. Statistical Arbitrage (Pairs Trading)
Trading the relative price spread between two cointegrated assets, remaining market-neutral.
- **Core Repositories**: Qlib, VectorBT, Lean.
- **Sub-Types**: Cointegration pairs trading, Portfolio-level stat-arb.
- **Evidence Grade**: B (Highly effective market-neutral strategy, but requires rigorous statistical validation and execution speed).

## 6. Funding / Basis Trading (Cash & Carry)
Capturing the difference between the spot asset price and the perpetual futures price (funding rate) while remaining delta-neutral.
- **Core Repositories**: Custom CCXT scripts, Freqtrade custom strategies.
- **Data Sources**: CoinGlass, CryptoQuant, Binance Futures Data.
- **Evidence Grade**: A (The most consistent and safest institutional crypto yield strategy).

## 7. Volatility & Options
Trading implied volatility, option spreads, or capturing the variance risk premium (VRP).
- **Core Repositories**: Deribit API integrations, Greeks.live (Data/Analytics).
- **Sub-Types**: Delta-neutral options market making, Gamma scalping.
- **Evidence Grade**: A (Highly profitable for specialized volatility traders, expanding market).

## 8. Orderbook & Microstructure (HFT)
Exploiting ultra-short-term imbalances in the Limit Order Book (LOB) to predict the next tick or optimize execution slippage.
- **Core Repositories**: DeepLOB, HftBacktest, NautilusTrader, Orderbook-rs, CryptoHFT.
- **Sub-Types**: Queue position estimation, Order flow imbalance (OFI), Toxicity detection.
- **Evidence Grade**: B+ (High alpha potential, but execution requires Rust/C++ and bare-metal co-location).

## 9. On-Chain, DEX, and MEV
Exploiting blockchain state dynamics, smart contract interactions, and mempool visibility.
- **Core Repositories**: Flashbots, Mev_Book (Awesome List), Jito (Solana).
- **Sub-Types**: Sandwiching, Frontrunning, DEX liquidations, Just-in-Time (JIT) liquidity.
- **Evidence Grade**: A (Extremely profitable for top searchers, highly adversarial).

## 10. Liquidation & Event-Driven
Trading based on specific market events, liquidations cascades, or news shocks.
- **Data Sources**: GDELT, CryptoPanic, CoinGlass (Liquidation heatmaps), Arkham Intelligence.
- **Sub-Types**: Short squeeze detection, Macro news shock trading, Token unlock plays.
- **Evidence Grade**: B (High burst profitability, difficult to automate perfectly).

## 11. ML Prediction (Tree Ensembles / Time-Series)
Using traditional machine learning models (XGBoost, LightGBM, Transformers) for feature-driven price prediction.
- **Core Repositories**: Qlib, FreqAI, Temporal Fusion Transformers (TFT), PatchTST.
- **Evidence Grade**: C+ (Heavy feature engineering required; raw price prediction models usually fail out-of-sample).

## 12. Reinforcement Learning (RL)
Using intelligent agents that learn optimal policies through trial and error in simulated market environments.
- **Core Repositories**: FinRL, FinRL-X (FinRL-Trading), Stable Baselines3.
- **Evidence Grade**: C (Massive sim-to-real gap; more viable for execution optimization than directional trading).

## 13. LLM & Agentic Systems
Utilizing Large Language Models as reasoning engines or autonomous trading agents.
- **Core Repositories**: OpenAlice, AI-Hedge-Fund (virattt), TradingAgents.
- **Evidence Grade**: D (Currently highly experimental and not safe for live unsupervised capital deployment).

## 14. Portfolio Allocation & Risk Management
Algorithms focused on optimal capital distribution and dynamic hedging rather than entry signals.
- **Core Repositories**: Qlib, VectorBT, PyPortfolioOpt.
- **Sub-Types**: Kelly Criterion sizing, Risk Parity, Hierarchical Risk Parity.
- **Evidence Grade**: A (Essential meta-layer for any strategy; dynamic sizing preserves capital).

## 15. Hybrid & Multi-Strategy
Ensemble systems combining multiple uncorrelated strategies and employing regime detection to switch between them.
- **Core Repositories**: Freqtrade (with regime filters), Lean.
- **Evidence Grade**: B+ (More robust than single-strategy approaches).

## 16. Automated Strategy Discovery (AutoML)
Using genetic programming or neural architecture search to automatically mine and discover trading rules or alpha factors.
- **Core Repositories**: RD-Agent (Qlib), gplearn, DEAP, Zenbot (Genetic algorithm tuner).
- **Evidence Grade**: B (Powerful for hypothesis generation, but requires stringent out-of-sample testing to prevent data mining bias).
