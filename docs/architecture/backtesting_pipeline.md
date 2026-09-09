# Backtesting Pipeline (Dual-Engine)

The cardinal rule of backtesting is Code Symmetry. The exact same strategy code that runs in production must run in the backtester.

## Engine A: Vectorized (Parameter Sweeper)
Target: VectorBT. Used exclusively for exploring massive parameter spaces in RAM. Path-independent. Not used for final validation.

## Engine B: Event-Driven (Live Simulator)
Target: NautilusTrader / Mocked EventBus. High-fidelity simulation of execution logic, queue position, slippage, and latency.

## Time-Travel Pattern
Instead of rewriting strategy logic, we swap the injected Providers:
1. `SimulatedClock` replaces system time.
2. `HistoricalDataReplayer` mocks the WebSocket feed and advances the simulated clock.
3. `MockMatchingEngine` intercepts order intents, simulates latency/slippage, and emits `broker.order_filled` events.
