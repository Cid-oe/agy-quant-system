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

class BinanceFeedProvider:
    """Mock WebSocket ingestor for Market Data Pipeline."""
    def __init__(self, bus: EventBus, logger: SystemLogger):
        self.bus = bus
        self.logger = logger
        self.running = False

    async def start(self):
        self.running = True
        self.logger.info("market_data_ingestion_started", exchange="Binance")
        while self.running:
            await asyncio.sleep(0.1) 
            tick = Tick(symbol="BTC/USDT", price=65000.0, volume=1.5, timestamp=0.0)
            await self.bus.publish(SystemEvent(topic="market_data.tick", payload=tick))

class TimeSeriesStorageDaemon:
    """Subscribes to market data and flushes to database in batches to bypass GIL."""
    def __init__(self, logger: SystemLogger):
        self.logger = logger
        self.buffer: List[Tick] = []
        self.BATCH_SIZE = 1000

    def handle_tick(self, event: SystemEvent):
        tick: Tick = event.payload
        self.buffer.append(tick)
        if len(self.buffer) >= self.BATCH_SIZE:
            asyncio.create_task(self.flush_to_db())

    async def flush_to_db(self):
        to_write = self.buffer
        self.buffer = []
        self.logger.info("db_flush", records=len(to_write), dest="ClickHouse_Mock")
