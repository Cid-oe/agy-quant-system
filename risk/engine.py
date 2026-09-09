import asyncio
from typing import Dict
from core.events import SystemEvent, EventBus

class RiskPolicyEngine:
    """The ultimate gatekeeper for all outgoing orders."""
    def __init__(self, bus: EventBus):
        self.bus = bus
        
        # Hardcoded Safety Limits
        self.MAX_ORDER_VALUE_USD = 50_000.0
        self.MAX_TOTAL_EXPOSURE_USD = 200_000.0
        self.MAX_DAILY_DRAWDOWN_PCT = 0.05  # 5%
        
        # Independent State Ledger
        self.current_exposure: Dict[str, float] = {}
        self.peak_equity = 1_000_000.0
        self.current_equity = 1_000_000.0
        
        self.bus.subscribe("execution.raw_order_request", self.evaluate_order)
        self.bus.subscribe("broker.portfolio_update", self._update_internal_state)

    async def evaluate_order(self, event: SystemEvent):
        order = event.payload
        order_value = order.price * order.quantity
        
        if order_value > self.MAX_ORDER_VALUE_USD:
            await self._reject(order, f"Fat Finger: Value {order_value} exceeds {self.MAX_ORDER_VALUE_USD}")
            return
            
        current_asset_exposure = self.current_exposure.get(order.symbol, 0.0)
        if order.side == "BUY" and (current_asset_exposure + order_value) > self.MAX_TOTAL_EXPOSURE_USD:
            await self._reject(order, f"Exposure Cap: Cannot add {order_value} to {current_asset_exposure}")
            return
            
        drawdown = (self.peak_equity - self.current_equity) / self.peak_equity
        if drawdown > self.MAX_DAILY_DRAWDOWN_PCT:
            await self._trigger_global_halt(f"Circuit Breaker: {drawdown*100}% drawdown exceeds limit.")
            return

        approved_event = SystemEvent(topic="risk.approved_order", payload=order)
        await self.bus.publish(approved_event)

    async def _reject(self, order, reason: str):
        rejection_event = SystemEvent(topic="risk.rejected_order", payload={"id": order.id, "reason": reason})
        await self.bus.publish(rejection_event)

    async def _update_internal_state(self, event: SystemEvent):
        portfolio = event.payload
        self.current_equity = portfolio.total_equity
        self.current_exposure = portfolio.asset_exposures
        if self.current_equity > self.peak_equity:
            self.peak_equity = self.current_equity

    async def _trigger_global_halt(self, reason: str):
        halt_event = SystemEvent(topic="system.emergency_halt", payload={"reason": reason})
        await self.bus.publish(halt_event)
