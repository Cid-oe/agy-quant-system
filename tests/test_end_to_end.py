"""
End-to-end Reality Anchor.
tick -> EventBus -> risk gate -> approved/rejected path.
If this file fails, the system is NOT ready.
"""
import asyncio
import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import SystemConfig
from core.logging import SystemLogger
from core.events import EventBus, SystemEvent
from risk.engine import RiskPolicyEngine
from data.pipeline import Tick

class MockOrder:
    def __init__(self, id, price, quantity, side):
        self.id = id; self.price = price
        self.quantity = quantity; self.side = side

@pytest.fixture
def logger():
    return SystemLogger(SystemConfig(environment="paper"))

@pytest.fixture
def risk(logger):
    e = RiskPolicyEngine(logger)
    e.sync_baseline(1_000_000.0)
    return e

# --- Risk Engine unit tests ---

def test_default_deny_before_sync(logger):
    e = RiskPolicyEngine(logger)
    assert e.halted is True
    assert e.evaluate(MockOrder("o1", 100.0, 1.0, "BUY")) is False

def test_approves_valid_order(risk):
    assert risk.evaluate(MockOrder("o2", 1000.0, 10.0, "BUY")) is True

def test_rejects_fat_finger(risk):
    assert risk.evaluate(MockOrder("o3", 60_000.0, 1.0, "BUY")) is False

def test_rejects_buy_exposure_breach(risk):
    risk.net_exposure = 195_000.0
    assert risk.evaluate(MockOrder("o4", 10_000.0, 1.0, "BUY")) is False

def test_rejects_sell_exposure_breach(risk):
    risk.gross_exposure = 395_000.0
    assert risk.evaluate(MockOrder("o5", 10_000.0, 1.0, "SELL")) is False

def test_halt_latches_and_does_not_reset(risk):
    risk.update_portfolio(930_000.0)   # 7% drawdown
    assert risk.halted is True
    risk.update_portfolio(1_010_000.0)  # Equity "recovers"
    assert risk.halted is True, "CRITICAL: Halt must latch. Only operator action clears it."

def test_rejects_malformed_order(risk):
    class BrokenOrder:
        id = "bad"
    assert risk.evaluate(BrokenOrder()) is False

def test_rejects_zero_value(risk):
    assert risk.evaluate(MockOrder("o6", 0.0, 100.0, "BUY")) is False
    assert risk.evaluate(MockOrder("o7", 100.0, 0.0, "BUY")) is False

def test_approved_order_updates_ledger(logger):
    e = RiskPolicyEngine(logger)
    e.sync_baseline(1_000_000.0)
    e.evaluate(MockOrder("o8", 1000.0, 5.0, "BUY"))
    assert e.net_exposure == 5_000.0
    assert e.gross_exposure == 5_000.0

def test_rejected_order_does_not_mutate_ledger(logger):
    e = RiskPolicyEngine(logger)
    e.sync_baseline(1_000_000.0)
    e.evaluate(MockOrder("o9", 60_000.0, 1.0, "BUY"))
    assert e.net_exposure == 0.0
    assert e.gross_exposure == 0.0

# --- EventBus integration tests ---

@pytest.mark.asyncio
async def test_eventbus_delivers_to_subscriber(logger):
    bus = EventBus(logger, max_size=100)
    received = []
    def handler(event): received.append(event.payload)
    bus.subscribe("market_data.tick", handler)
    task = asyncio.create_task(bus.start())
    tick = Tick("BTC/USDT", 65000.0, 1.5, 0.0)
    await bus.publish(SystemEvent("market_data.tick", tick))
    await asyncio.sleep(0.2)
    await bus.stop()
    task.cancel()
    assert len(received) == 1
    assert received[0].symbol == "BTC/USDT"

@pytest.mark.asyncio
async def test_bounded_queue_signals_overflow(logger):
    bus = EventBus(logger, max_size=1)
    event = SystemEvent("market_data.tick", "x")
    first  = await bus.publish(event, block=False)
    second = await bus.publish(event, block=False)
    assert first is True
    assert second is False, "Bounded queue must signal caller on overflow."
