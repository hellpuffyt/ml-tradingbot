"""MLTrader wiring with stubbed broker methods and a stubbed news client (no network, no orders)."""

from datetime import datetime
from types import SimpleNamespace

import pytest

import tradingbot as tb  # regression: importing used to construct a broker and run a backtest


class FakeTrader:
    def __init__(self, cash, price, sentiment, last_trade=None):
        self.symbol, self.cash_at_risk, self.last_trade = "SPY", 0.05, last_trade
        self._cash, self._price, self._sentiment = cash, price, sentiment
        self.orders, self.sold_all = [], False

    def get_cash(self):
        return self._cash

    def get_last_price(self, symbol):
        return self._price

    def get_sentiment(self):
        return self._sentiment

    def sell_all(self):
        self.sold_all = True

    def create_order(self, *args, **kwargs):
        return (args, kwargs)

    def submit_order(self, order):
        self.orders.append(order)

    position_sizing = tb.MLTrader.position_sizing


def test_iteration_submits_bracket_buy():
    t = FakeTrader(100_000, 500, (0.9999, "positive"))
    tb.MLTrader.on_trading_iteration(t)
    (args, kwargs), = t.orders
    assert args == ("SPY", 10, "buy")
    assert kwargs["type"] == "bracket"
    assert kwargs["take_profit_price"] == pytest.approx(600)
    assert kwargs["stop_loss_price"] == pytest.approx(475)
    assert t.last_trade == "buy" and not t.sold_all


def test_iteration_closes_short_before_going_long():
    t = FakeTrader(100_000, 500, (0.9999, "positive"), last_trade="sell")
    tb.MLTrader.on_trading_iteration(t)
    assert t.sold_all and t.last_trade == "buy"


def test_iteration_holds_on_neutral():
    t = FakeTrader(100_000, 500, (1.0, "neutral"))
    tb.MLTrader.on_trading_iteration(t)
    assert t.orders == [] and t.last_trade is None


def test_fetch_headlines_uses_news_request():
    seen = {}

    class FakeClient:
        def get_news(self, req):
            seen["req"] = req
            return SimpleNamespace(data={"news": [SimpleNamespace(headline="SPY rallies")]})

    out = tb.fetch_headlines(FakeClient(), "SPY", datetime(2025, 1, 1), datetime(2025, 1, 4))
    assert out == ["SPY rallies"]
    assert seen["req"].symbols == ["SPY"] or seen["req"].symbols == "SPY"


def test_parse_args_validates():
    a = tb.parse_args(["--start", "2025-01-01", "--end", "2025-02-01"])
    assert a.symbol == "SPY" and a.cash_at_risk == 0.05
    with pytest.raises(SystemExit):
        tb.parse_args(["--start", "2025-02-01", "--end", "2025-01-01"])
    with pytest.raises(SystemExit):
        tb.parse_args(["--cash-at-risk", "2"])


def test_main_refuses_without_credentials(monkeypatch):
    for k in ("ALPACA_API_KEY", "ALPACA_API_SECRET", "ALPACA_PAPER"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setattr(tb.MLTrader, "backtest", lambda *a, **k: pytest.fail("must not backtest"))
    with pytest.raises(SystemExit, match="ALPACA_API_KEY"):
        tb.main([])
