# Risk & Policy Engine (C16)

The ultimate gatekeeper and most critical infrastructure component.

## Architectural Mandates
1. Strict Isolation: Strategies do not generate OrderRequests, only StrategyIntents. The Execution Engine translates intents into orders, which the Risk Engine intercepts.
2. State Sovereignty: Risk Engine maintains its own parallel ledger. It does not trust Strategy accounting.
3. Default Deny: If Risk Engine lags or crashes, trading halts.
4. Kill Switches: Global equity curve monitoring severs exchange connectivity on Max Drawdown breach.

## Defenses
- Fat-Finger Filter (Max order value)
- Max Exposure Cap (Max % of equity per asset)
- Drawdown Halt (Circuit breaker)
- API Rate Limit Token Bucket (Prevents HTTP 429 bans)
