import asyncio
from dataclasses import dataclass
from typing import Any, Callable, Dict, List
from .logging import SystemLogger

@dataclass
class SystemEvent:
    topic: str
    payload: Any
    timestamp: float = 0.0

EventHandler = Callable[[SystemEvent], None]

class EventBus:
    def __init__(self, logger: SystemLogger):
        self._subscribers: Dict[str, List[EventHandler]] = {}
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=10000)
        self._logger = logger
        self._running = False

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(handler)
        self._logger.info("bus_subscribed", topic=topic, handler=handler.__name__)

    async def publish(self, event: SystemEvent) -> None:
        if self._queue.full():
            self._logger.error("bus_overload", Exception("EventBus queue full, dropping event"), topic=event.topic)
            return
        await self._queue.put(event)

    async def start(self):
        self._running = True
        self._logger.info("event_bus_started")
        while self._running:
            event = await self._queue.get()
            handlers = self._subscribers.get(event.topic, [])
            for handler in handlers:
                try:
                    asyncio.create_task(self._safe_execute(handler, event))
                except Exception as e:
                    self._logger.error("bus_handler_error", e, topic=event.topic)
            self._queue.task_done()

    async def _safe_execute(self, handler: EventHandler, event: SystemEvent):
        if asyncio.iscoroutinefunction(handler):
            await handler(event)
        else:
            handler(event)

    def stop(self):
        self._running = False
        self._logger.info("event_bus_stopped")
