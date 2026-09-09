# System Premortem & Refinements

**Most Likely Failure**: asyncio Event Loop Saturation.
*Fix*: EventBus must use bounded queues (maxsize). Inference (ML) must run in `ProcessPoolExecutor` to avoid blocking the main I/O loop.

**Most Dangerous Failure**: Risk Engine "Split Brain".
*Fix*: Risk Engine cannot rely solely on WebSocket `order_filled` events. Must have an active 30-second REST API reconciliation loop.

**Critical Boot Sequence**: System cannot start trading until Risk Engine explicitly queries exchange REST API and populates baseline equity.
