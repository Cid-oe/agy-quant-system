# Market Data Pipeline (Zero-Block EDA)

The Market Data Pipeline must operate strictly on a Producer/Consumer model using the EventBus to prevent Python GIL lockups.

## Flow
[External Exchange WebSocket] -> [Feed Connector (Producer)] -> [EventBus ('raw_tick')]
-> [Live Strategy (Consumer)]
-> [Storage Daemon (Consumer)]

## Rules
1. Feed Connector MUST NEVER write directly to a database. It only calls `bus.publish`.
2. Feed Connector MUST handle WebSocket disconnects, ping/pong heartbeats, and sequence ID tracking.
3. Storage Daemon batches ticks into memory (e.g. 1000 records) and asynchronously flushes to ClickHouse/DuckDB to avoid I/O blocking.
