"""
Basis / Funding Rate Arbitrage Strategy (C20)
Grade A - Highest Conviction Edge per technical-implementation-blueprint.md

Delta-neutral cash-and-carry: hold spot long + perpetual short.
Profit accrues from positive funding rate payments every 8 hours.

SAFETY CONTRACT:
- All orders MUST pass through RiskPolicyEngine.evaluate() before execution.
- Strategy only emits StrategyIntent events. It never touches the Broker directly.
- Strategy halts automatically when funding rate flips negative.
"""

from dataclasses import dataclass
from typing import Optional
from core.events import EventBus, SystemEvent
from core.logging import SystemLogger


FUNDING_THRESHOLD = 0.0001   # Minimum 0.01% per 8h to enter
FUNDING_EXIT_THRESHOLD = 0.0  # Exit if rate goes to zero or negative


@dataclass
class FundingRateUpdate:
    symbol: str
    rate: float          # Per 8h, e.g. 0.0003 = 0.03%
    next_payment_ts: float


@dataclass
class StrategyIntent:
    strategy_id: str
    symbol: str
    spot_side: str        # BUY (long spot)
    perp_side: str        # SELL (short perp)
    notional_usd: float
    reason: str


class BasisFundingStrategy:
    """
    Delta-neutral funding rate arbitrage.
    Subscribes to funding rate updates. Emits StrategyIntent when edge exists.
    """

    STRATEGY_ID = "basis_funding_v1"

    def __init__(self, bus: EventBus, logger: SystemLogger,
                 target_notional_usd: float = 10_000.0):
        self.bus = bus
        self.logger = logger
        self.target_notional = target_notional_usd
        self.in_position = False
        self.current_rate: Optional[float] = None

        # Subscribe to funding rate feed (emitted by C13 FundingRateMonitor)
        self.bus.subscribe("market_data.funding_rate", self._on_funding_rate)
        self.logger.info("basis_strategy_initialized",
                         target_notional=target_notional_usd)

    def _on_funding_rate(self, event: SystemEvent):
        update: FundingRateUpdate = event.payload
        self.current_rate = update.rate

        if not self.in_position and update.rate >= FUNDING_THRESHOLD:
            self._enter_position(update)

        elif self.in_position and update.rate <= FUNDING_EXIT_THRESHOLD:
            self._exit_position(update)

    def _enter_position(self, update: FundingRateUpdate):
        """Emit an intent to enter a delta-neutral long spot / short perp position."""
        intent = StrategyIntent(
            strategy_id=self.STRATEGY_ID,
            symbol=update.symbol,
            spot_side="BUY",
            perp_side="SELL",
            notional_usd=self.target_notional,
            reason=f"Funding rate {update.rate:.4%} >= threshold {FUNDING_THRESHOLD:.4%}"
        )
        self.in_position = True
        self.logger.info("basis_intent_enter",
                         symbol=update.symbol, rate=update.rate)
        import asyncio
        asyncio.create_task(self.bus.publish(
            SystemEvent(topic="strategy.intent", payload=intent)
        ))

    def _exit_position(self, update: FundingRateUpdate):
        """Emit an intent to exit the position when funding flips non-positive."""
        intent = StrategyIntent(
            strategy_id=self.STRATEGY_ID,
            symbol=update.symbol,
            spot_side="SELL",
            perp_side="BUY",
            notional_usd=self.target_notional,
            reason=f"Funding rate {update.rate:.4%} <= exit threshold. Closing."
        )
        self.in_position = False
        self.logger.info("basis_intent_exit",
                         symbol=update.symbol, rate=update.rate)
        import asyncio
        asyncio.create_task(self.bus.publish(
            SystemEvent(topic="strategy.intent", payload=intent)
        ))
