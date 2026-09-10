import inspect
import asyncio
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List
from core.logging import SystemLogger


@dataclass
class SystemEvent:
    topic: str
    payload: Any
    timestamp: float = field(default_factory=time.time)


EventHandler = Callable[[SystemEvent], None]


class EventBus:
    """
    Async pub/sub bus with per-topic sequential dispatch.
    Bounded queue — publish(block=False) returns False on overflow rather than dropping silently.
    """
    def __init__(self, logger: SystemLogger, max_size: int = 1000):
        self._logger      = logger
        self._max_size    = max_size
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=max_size)
        self._subscribers: Dict[str, List[EventHandler]] = {}
        self._topic_queues: Dict[str, asyncio.Queue] = {}
        self._topic_tasks: List[asyncio.Task] = []
        self._running = False

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        if topic not in self._subscribers:
            self._subscribers[topic] = []
            self._topic_queues[topic] = asyncio.Queue(maxsize=self._max_size)
        self._subscribers[topic].append(handler)
        self._logger.info("bus_subscribed", topic=topic, handler=handler.__name__)

    async def publish(self, event: SystemEvent, block: bool = True) -> bool:
        try:
            if block:
                await self._queue.put(event)
            else:
                self._queue.put_nowait(event)
            return True
        except asyncio.QueueFull:
            self._logger.error("bus_queue_full", Exception("Queue full — dropping event"), topic=event.topic)
            return False

    async def start(self):
        self._running = True
        loop = asyncio.get_running_loop()
        loop.set_exception_handler(self._handle_loop_exception)

        for topic, q in self._topic_queues.items():
            t = asyncio.create_task(self._topic_worker(topic, q))
            self._topic_tasks.append(t)

        self._logger.info("event_bus_started", topics=list(self._topic_queues.keys()))

        while self._running:
            try:
                event = await self._queue.get()
                if event.topic == "__poison__":
                    self._queue.task_done()
                    break
                if event.topic in self._topic_queues:
                    await self._topic_queues[event.topic].put(event)
                self._queue.task_done()
            except asyncio.CancelledError:
                break

    async def _topic_worker(self, topic: str, q: asyncio.Queue):
        while self._running:
            event = await q.get()
            if event.topic == "__poison__":
                q.task_done()
                break
            for handler in self._subscribers.get(topic, []):
                try:
                    if inspect.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                except Exception as e:
                    self._logger.error("handler_exception", e, topic=topic,
                                       handler=handler.__name__)
            q.task_done()

    def _handle_loop_exception(self, loop, context):
        exc = context.get("exception", Exception(context.get("message", "unknown")))
        self._logger.error("unhandled_loop_exception", exc)

    async def stop(self):
        self._running = False
        await self._queue.put(SystemEvent("__poison__", None))
        for q in self._topic_queues.values():
            await q.put(SystemEvent("__poison__", None))
        self._logger.info("event_bus_stopped")
