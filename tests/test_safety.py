"""Static guards: no live-trading endpoint, no live trader, no credentials in source."""

import re

from conftest import REPO

SOURCES = sorted(p for p in REPO.glob("*.py"))


def test_no_live_trading_endpoint_in_code():
    for path in SOURCES:
        assert "://api.alpaca.markets" not in path.read_text(), path.name


def test_no_live_trader_or_broker_is_constructed():
    text = (REPO / "tradingbot.py").read_text()
    assert "lumibot.traders" not in text and not re.search(r"\bTrader\(", text)
    assert "lumibot.brokers" not in text


def test_no_credentials_assigned_in_source():
    # Regression: real paper keys were once hard-coded in tradingbot.py.
    pattern = re.compile(r"""(API_KEY|API_SECRET|SECRET_KEY)\s*=\s*["'][^"']+["']""")
    for path in SOURCES:
        assert not pattern.search(path.read_text()), path.name
