"""Pure trading-signal and configuration logic (no broker, no network, no model).

Kept separate from ``tradingbot.py`` so it can be unit-tested without LumiBot,
Alpaca or FinBERT.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

# Only the paper-trading endpoint is ever used. This project has no live-trading path.
PAPER_BASE_URL = "https://paper-api.alpaca.markets"

SENTIMENT_THRESHOLD = 0.999
TAKE_PROFIT_LONG = 1.20  # +20 % for a long position
STOP_LOSS_LONG = 0.95  # -5 % for a long position
TAKE_PROFIT_SHORT = 0.80  # mirror of the long bracket for a short position
STOP_LOSS_SHORT = 1.05

_FALSE = {"0", "false", "no", "off"}


@dataclass(frozen=True)
class Signal:
    side: str  # "buy" or "sell"
    quantity: int
    take_profit_price: float
    stop_loss_price: float
    close_existing: bool  # close the opposite position before entering


def position_size(cash: float, last_price: float, cash_at_risk: float) -> int:
    """Whole shares worth ``cash_at_risk`` of the available cash (0 if not even one share)."""
    if last_price <= 0 or cash <= 0 or not 0 < cash_at_risk <= 1:
        return 0
    return int(cash * cash_at_risk / last_price)


def decide(
    sentiment: str,
    probability: float,
    cash: float,
    last_price: float,
    quantity: int,
    last_trade: str | None,
    threshold: float = SENTIMENT_THRESHOLD,
) -> Signal | None:
    """Return the order to place for this iteration, or ``None`` to hold."""
    if quantity < 1 or cash <= last_price:
        return None
    if probability <= threshold:
        return None
    if sentiment == "positive":
        return Signal(
            "buy",
            quantity,
            last_price * TAKE_PROFIT_LONG,
            last_price * STOP_LOSS_LONG,
            close_existing=last_trade == "sell",
        )
    if sentiment == "negative":
        return Signal(
            "sell",
            quantity,
            last_price * TAKE_PROFIT_SHORT,
            last_price * STOP_LOSS_SHORT,
            close_existing=last_trade == "buy",
        )
    return None


def load_credentials(environ: Mapping[str, str] | None = None) -> dict:
    """Read Alpaca credentials from the environment only.

    Raises ``SystemExit`` if they are missing, or if live trading is requested
    (``ALPACA_PAPER`` set to a false value): this project only supports paper
    credentials and simulated backtests.
    """
    environ = os.environ if environ is None else environ
    key = environ.get("ALPACA_API_KEY", "").strip()
    secret = environ.get("ALPACA_API_SECRET", "").strip()
    if environ.get("ALPACA_PAPER", "true").strip().lower() in _FALSE:
        raise SystemExit(
            "ALPACA_PAPER=false requested live trading. This project does not support "
            "live trading; use paper-trading API keys."
        )
    if not key or not secret:
        raise SystemExit(
            "Set ALPACA_API_KEY and ALPACA_API_SECRET (paper-trading keys) in the "
            "environment; see .env.example. Keys are never read from source files."
        )
    return {"API_KEY": key, "API_SECRET": secret, "PAPER": True}
