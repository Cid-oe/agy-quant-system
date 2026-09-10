#!/bin/bash
cd /home/cid/agy-quant-system

cat << 'PYEOF' > core/config.py
import os
import json
from pydantic import BaseModel, Field

class SystemConfig(BaseModel):
    environment: str = Field(default="paper")
    log_level: str = Field(default="INFO")
    db_uri: str = Field(default="sqlite:///:memory:")
    plugins: list[str] = Field(default_factory=list)
    custom: dict = Field(default_factory=dict)

class ConfigLoader:
    @staticmethod
    def load(path: str = "config.json") -> SystemConfig:
        if os.path.exists(path):
            with open(path, "r") as f:
                return SystemConfig(**json.load(f))
        return SystemConfig()
PYEOF

cat << 'PYEOF' > core/events.py
import asyncio
import time
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
    def __init__(self, logger: SystemLogger, max_size=1000):
        self._subscribers: Dict[str, List[EventHandler]] = {}
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=max_size)
        self._logger = logger
        self._running = False
        self._topic_queues = {}
        self._topic_tasks = []

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        if topic not in self._subscribers:
            self._subscribers[topic] = []
            self._topic_queues[topic] = asyncio.Queue(maxsize=1000)
        self._subscribers[topic].append(handler)
        self._logger.info("bus_subscribed", topic=topic, handler=handler.__name__)

    async def publish(self, event: SystemEvent, block=True) -> bool:
        if not event.timestamp:
            event.timestamp = time.time()
        try:
            if block:
                await self._queue.put(event)
            else:
                self._queue.put_nowait(event)
            return True
        except asyncio.QueueFull:
            self._logger.error("bus_overload", Exception("Queue full"), topic=event.topic)
            return False

    async def start(self):
        self._running = True
        loop = asyncio.get_running_loop()
        loop.set_exception_handler(self._handle_exception)
        
        for topic, q in self._topic_queues.items():
            self._topic_tasks.append(asyncio.create_task(self._topic_worker(topic, q)))
            
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
            for handler in self._subscribers.get(event.topic, []):
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                except Exception as e:
                    self._logger.error("bus_handler_error", e, topic=event.topic)
            q.task_done()

    def _handle_exception(self, loop, context):
        msg = context.get("exception", context["message"])
        self._logger.error("unhandled_async_exception", Exception(str(msg)))

    async def stop(self):
        self._running = False
        await self.publish(SystemEvent("__poison__", None), block=True)
        for q in self._topic_queues.values():
            await q.put(SystemEvent("__poison__", None))
PYEOF

cat << 'PYEOF' > core/plugins.py
import importlib
from typing import List, Protocol
from .registry import ProviderRegistry
from .events import EventBus
from .logging import SystemLogger

class PluginProtocol(Protocol):
    def initialize(self, registry: ProviderRegistry, bus: EventBus) -> None: ...

class PluginLoader:
    def __init__(self, registry: ProviderRegistry, bus: EventBus, logger: SystemLogger):
        self.registry = registry
        self.bus = bus
        self.logger = logger

    def load_all(self, plugin_paths: List[str]):
        for path in plugin_paths:
            try:
                module = importlib.import_module(path)
                plugin: PluginProtocol = getattr(module, "Plugin")()
                plugin.initialize(self.registry, self.bus)
                self.logger.info("plugin_loaded", plugin=path)
            except Exception as e:
                self.logger.error("plugin_load_failed_fatal", e, plugin=path)
                raise SystemExit(f"FATAL: Plugin {path} failed to load.")
PYEOF

cat << 'PYEOF' > risk/engine.py
from typing import Any
from core.logging import SystemLogger

class RiskPolicyEngine:
    def __init__(self, logger: SystemLogger):
        self.logger = logger
        self.MAX_ORDER_VALUE_USD = 50_000.0
        self.MAX_TOTAL_EXPOSURE_USD = 200_000.0
        self.MAX_DAILY_DRAWDOWN_PCT = 0.05
        
        self.net_exposure = 0.0
        self.gross_exposure = 0.0
        self.peak_equity = 0.0
        self.current_equity = 0.0
        self.halted = True # Default Deny until baseline synced
        
    def sync_baseline(self, equity: float):
        self.peak_equity = equity
        self.current_equity = equity
        self.halted = False
        self.logger.info("risk_engine_synced", equity=equity)

    def evaluate(self, order: Any) -> bool:
        if self.halted:
            return False
            
        try:
            order_value = getattr(order, 'price', 0.0) * getattr(order, 'quantity', 0.0)
            if order_value <= 0:
                self.logger.error("risk_reject", Exception("Invalid value"), id=getattr(order, 'id', ''))
                return False
                
            if order_value > self.MAX_ORDER_VALUE_USD:
                self.logger.error("risk_reject", Exception("Fat Finger"), val=order_value)
                return False
                
            is_buy = getattr(order, 'side', '') == 'BUY'
            delta = order_value if is_buy else -order_value
            
            new_net = self.net_exposure + delta
            new_gross = self.gross_exposure + order_value
            
            if abs(new_net) > self.MAX_TOTAL_EXPOSURE_USD or new_gross > self.MAX_TOTAL_EXPOSURE_USD * 2:
                self.logger.error("risk_reject", Exception("Exposure cap"), net=new_net)
                return False
                
            self.net_exposure = new_net
            self.gross_exposure = new_gross
            return True
            
        except Exception as e:
            self.logger.error("risk_reject_exception", e)
            return False
            
    def update_portfolio(self, equity: float):
        self.current_equity = equity
        if self.current_equity > self.peak_equity:
            self.peak_equity = self.current_equity
            
        if self.peak_equity > 0:
            drawdown = (self.peak_equity - self.current_equity) / self.peak_equity
            if drawdown > self.MAX_DAILY_DRAWDOWN_PCT:
                self.halted = True
                self.logger.error("system_halted_latch", Exception(f"Drawdown {drawdown}"))
PYEOF

cat << 'PYEOF' > data/pipeline.py
import asyncio
from typing import List
from dataclasses import dataclass
from core.events import SystemEvent, EventBus
from core.logging import SystemLogger

@dataclass(slots=True)
class Tick:
    symbol: str
    price: float
    volume: float
    timestamp: float

class TimeSeriesStorageDaemon:
    def __init__(self, logger: SystemLogger):
        self.logger = logger
        self.buffer: List[Tick] = []
        self.BATCH_SIZE = 1000
        self.running = False

    async def start(self):
        self.running = True
        while self.running:
            await asyncio.sleep(5)
            await self.flush_to_db()

    def handle_tick(self, event: SystemEvent):
        self.buffer.append(event.payload)
        if len(self.buffer) >= self.BATCH_SIZE:
            asyncio.create_task(self.flush_to_db())

    async def flush_to_db(self):
        if not self.buffer: return
        to_write = self.buffer
        self.buffer = []
        try:
            self.logger.info("db_flush", records=len(to_write))
        except Exception as e:
            self.logger.error("db_flush_error", e)
            self.buffer = to_write + self.buffer
            
    async def stop(self):
        self.running = False
        await self.flush_to_db()
PYEOF

chmod +x fix_repo.sh
./fix_repo.sh
