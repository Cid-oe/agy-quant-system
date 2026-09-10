# Open Issues (Premortem Action Items)

These are required before any live capital is deployed.

## P0 — Critical (Blocks Live Trading)

- [ ] **ISSUE-001**: REST baseline sync not implemented. `risk/engine.py:sync_baseline()` currently accepts a hardcoded value. Must call exchange REST API on boot and refuse to trade until confirmed.
- [ ] **ISSUE-002**: No API rate-limit token bucket. The Risk Engine does not track requests/minute. A rogue strategy can trigger an exchange HTTP 429 ban with open positions.
- [ ] **ISSUE-003**: No SIGTERM handler. `bus.stop()` is never called on Ctrl+C or OS kill. Open positions are left unmanaged on shutdown.
- [ ] **ISSUE-004**: `BinanceFeedProvider` is a mock. Real CCXT Pro WebSocket connection with reconnect/heartbeat/sequence-ID tracking is not implemented.
- [ ] **ISSUE-011**: No price sanity check (T08). Fat-finger filter only checks notional. Need a price-vs-market band.
- [ ] **ISSUE-012**: No idempotency tracking (T09). Same order.id can be approved twice.
- [ ] **ISSUE-013**: The breaker halts risk-reducing trades (T07). A SELL to flatten a long position is rejected if the system is halted.
- [ ] **ISSUE-014**: Risk state has no backing store (T22). Restarts fabricate a flat ledger.

## P1 — High (Blocks Paper Trading Validation)

- [ ] **ISSUE-005**: `strategies/basis/` is empty. The highest-conviction edge (funding rate basis) has no implementation.
- [ ] **ISSUE-006**: No `docker-compose.yml`. Arena Agent has no reproducible environment for ClickHouse/Redis.
- [ ] **ISSUE-007**: `TimeSeriesStorageDaemon` writes to a log line, not a real database. ClickHouse schema in `storage/clickhouse/` is empty.
- [ ] **ISSUE-015**: `SystemEvent.timestamp` defaults to `0.0` (T19/T20). Feed needs to set event-id and timestamp for gap detection.
- [ ] **ISSUE-016**: No typed contracts (T19/T20). `Order`, `Position`, `StrategyIntent` need Pydantic schemas to prevent drift.

## P2 — Medium (Architecture Debt)

- [ ] **ISSUE-008**: Drawdown check only runs on order arrival. An idle strategy that bleeds 30% triggers no monitoring.
- [ ] **ISSUE-009**: `MAX_DAILY_DRAWDOWN_PCT` has no day boundary — currently all-time peak. Add UTC midnight reset.
- [ ] **ISSUE-010**: `structlog` is declared in requirements but 0 imports. Replace stdlib `logging` with `structlog` for structured JSON logs with trace-ids.
- [ ] **ISSUE-017**: Plugin load failure swallows errors in boot (T26). Needs to strictly fail if required plugins aren't ready.
