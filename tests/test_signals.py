import pytest

import signals as s


def test_positive_sentiment_buys_with_long_bracket():
    sig = s.decide("positive", 0.9995, cash=10_000, last_price=100, quantity=5, last_trade=None)
    assert sig == s.Signal("buy", 5, pytest.approx(120.0), pytest.approx(95.0), close_existing=False)


def test_negative_sentiment_shorts_when_cash_is_available():
    # Regression: the negative branch was attached to `if cash > last_price` as an
    # `elif`, so it only ran when the account could NOT afford one share.
    sig = s.decide("negative", 0.9995, cash=10_000, last_price=100, quantity=5, last_trade=None)
    assert sig is not None and sig.side == "sell"
    assert sig.take_profit_price == pytest.approx(80.0)
    assert sig.stop_loss_price == pytest.approx(105.0)


def test_negative_sentiment_without_cash_does_nothing():
    assert s.decide("negative", 0.9995, cash=50, last_price=100, quantity=1, last_trade=None) is None


def test_flip_from_short_to_long_closes_the_short_first():
    # Regression: compared last_trade with "Sell" but stored "sell", so a short was never closed.
    sig = s.decide("positive", 0.9995, cash=10_000, last_price=100, quantity=5, last_trade="sell")
    assert sig.close_existing is True


def test_flip_from_long_to_short_closes_the_long_first():
    sig = s.decide("negative", 0.9995, cash=10_000, last_price=100, quantity=5, last_trade="buy")
    assert sig.close_existing is True


@pytest.mark.parametrize("sentiment,prob", [("neutral", 1.0), ("positive", 0.999), ("negative", 0.5)])
def test_holds_below_threshold_or_neutral(sentiment, prob):
    assert s.decide(sentiment, prob, cash=10_000, last_price=100, quantity=5, last_trade=None) is None


def test_position_size_never_exceeds_cash_at_risk():
    # Regression: max(1, ...) bought a whole share even when 5 % of cash was less than its price.
    assert s.position_size(cash=1_000, last_price=500, cash_at_risk=0.05) == 0
    assert s.position_size(cash=100_000, last_price=500, cash_at_risk=0.05) == 10
    assert s.decide("positive", 1.0, cash=1_000, last_price=500, quantity=0, last_trade=None) is None


@pytest.mark.parametrize("cash,price,risk", [(0, 100, 0.05), (100, 0, 0.05), (100, 10, 0), (100, 10, 1.5)])
def test_position_size_rejects_invalid_inputs(cash, price, risk):
    assert s.position_size(cash, price, risk) == 0


def test_credentials_come_from_environment_and_are_paper_only():
    key, secret = "PK" + "TEST0000", "s" * 8
    creds = s.load_credentials({"ALPACA_API_KEY": key, "ALPACA_API_SECRET": secret})
    assert creds == {"API_KEY": key, "API_SECRET": secret, "PAPER": True}


def test_missing_credentials_refuse_to_start():
    with pytest.raises(SystemExit, match="ALPACA_API_KEY"):
        s.load_credentials({})


@pytest.mark.parametrize("value", ["false", "0", "no", "OFF"])
def test_live_trading_request_is_refused(value):
    env = {"ALPACA_API_KEY": "k", "ALPACA_API_SECRET": "s", "ALPACA_PAPER": value}
    with pytest.raises(SystemExit, match="live trading"):
        s.load_credentials(env)
