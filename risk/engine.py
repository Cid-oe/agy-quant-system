from typing import Any, Set
from core.logging import SystemLogger


class RiskPolicyEngine:
    """
    Synchronous, inline risk gate. Default Deny until sync_baseline() is called.
    ALL orders MUST call evaluate() and receive True before reaching the broker.
    No EventBus dependency — operates in-line in the caller's task.
    """
    def __init__(self, logger: SystemLogger):
        self.logger = logger
        self.MAX_ORDER_VALUE_USD   = 50_000.0
        self.MAX_NET_EXPOSURE_USD  = 200_000.0
        self.MAX_GROSS_EXPOSURE_USD = 400_000.0   # 2x net cap covers both legs
        self.MAX_DAILY_DRAWDOWN_PCT = 0.05
        
        # New Price/Market Band Check (T08)
        self.MAX_PRICE_DEVIATION_PCT = 0.10

        self.net_exposure   = 0.0
        self.gross_exposure = 0.0
        self.peak_equity    = 0.0
        self.current_equity = 0.0
        self.halted = True   # Default Deny until REST baseline confirmed
        
        # T09 Idempotency tracking
        self._processed_orders: Set[str] = set()
        
        # T22 Persistence mock
        self._state_file = "/tmp/risk_state.json"

    def sync_baseline(self, equity: float):
        """Must be called with live exchange REST balance before any trading starts."""
        if equity <= 0:
            raise ValueError("Baseline equity must be positive.")
        self.peak_equity    = equity
        self.current_equity = equity
        self.halted = False
        self.logger.info("risk_engine_synced", equity=equity)

    def evaluate(self, order: Any, current_market_price: float = None) -> bool:
        """
        Synchronous gate. Returns True only if all checks pass.
        Any exception, missing field, or limit breach → False (Default Deny).
        """
        order_id = getattr(order, 'id', None)
        
        # T09 Idempotency Check
        if order_id and order_id in self._processed_orders:
            self.logger.error("risk_reject_idempotency", Exception("Order ID already processed"), id=order_id)
            return False

        try:
            price    = float(getattr(order, 'price',    0.0))
            quantity = float(getattr(order, 'quantity', 0.0))
            side     = str(getattr(order,   'side',     ''))

            order_value = price * quantity
            if order_value <= 0:
                self.logger.error("risk_reject_zero_value", Exception("price*qty<=0"), id=order_id)
                return False

            if order_value > self.MAX_ORDER_VALUE_USD:
                self.logger.error("risk_reject_fat_finger", Exception("Exceeds max order value"), value=order_value)
                return False
                
            # T08 Price Sanity Check
            if current_market_price and price > 0:
                deviation = abs(price - current_market_price) / current_market_price
                if deviation > self.MAX_PRICE_DEVIATION_PCT:
                    self.logger.error("risk_reject_price_band", Exception("Price deviates from market"), dev=deviation)
                    return False

            delta    = order_value if side == "BUY" else -order_value
            new_net  = self.net_exposure  + delta
            new_gross = self.gross_exposure + order_value
            
            # T07 Risk-Reducing Trade Exemption
            is_risk_reducing = (side == "SELL" and self.net_exposure > 0) or (side == "BUY" and self.net_exposure < 0)

            if self.halted and not is_risk_reducing:
                self.logger.error("risk_reject_halted", Exception("Engine is halted"), id=order_id)
                return False

            if abs(new_net) > self.MAX_NET_EXPOSURE_USD:
                self.logger.error("risk_reject_net_exposure", Exception("Net cap breach"), new_net=new_net)
                return False

            if new_gross > self.MAX_GROSS_EXPOSURE_USD:
                self.logger.error("risk_reject_gross_exposure", Exception("Gross cap breach"), new_gross=new_gross)
                return False

            # All checks passed — atomically reserve exposure
            self.net_exposure   = new_net
            self.gross_exposure = new_gross
            
            if order_id:
                self._processed_orders.add(order_id)
                
            return True

        except Exception as e:
            self.logger.error("risk_reject_exception", e)
            return False

    def settle(self, order: Any, filled_value: float):
        """Call after confirmed broker fill to reconcile the ledger."""
        side  = str(getattr(order, 'side', ''))
        delta = filled_value if side == "BUY" else -filled_value
        self.net_exposure   += delta
        self.gross_exposure += filled_value

    def update_portfolio(self, equity: float):
        """
        Called on every portfolio update event.
        Latching halt: once tripped, only an explicit operator reset clears it.
        """
        self.current_equity = equity
        if equity > self.peak_equity:
            self.peak_equity = equity

        if self.peak_equity > 0:
            drawdown = (self.peak_equity - self.current_equity) / self.peak_equity
            if drawdown > self.MAX_DAILY_DRAWDOWN_PCT and not self.halted:
                self.halted = True
                self.logger.error("circuit_breaker_halt",
                                  Exception(f"Drawdown {drawdown:.2%} breached {self.MAX_DAILY_DRAWDOWN_PCT:.2%}"))

    def operator_reset_halt(self):
        """Explicit operator action required to re-enable after a halt. Never automated."""
        self.halted = False
        self.logger.info("risk_halt_manually_cleared")
