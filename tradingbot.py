"""Sentiment-driven SPY strategy, run as a SIMULATED backtest only.

Educational code. It never places real orders: the only entry point is a LumiBot
backtest on historical Yahoo Finance prices. Alpaca paper-trading keys (from the
environment) are used solely to download historical news headlines.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta

from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy

from finbert_utils import estimate_sentiment
from signals import decide, load_credentials, position_size

NEWS_LOOKBACK_DAYS = 3


def make_news_client(creds: dict):
    """Historical-news client for Alpaca's market-data API (read-only)."""
    from alpaca.data.historical.news import NewsClient

    return NewsClient(api_key=creds["API_KEY"], secret_key=creds["API_SECRET"])


def fetch_headlines(client, symbol: str, start: datetime, end: datetime) -> list[str]:
    from alpaca.data.requests import NewsRequest

    news_set = client.get_news(NewsRequest(symbols=symbol, start=start, end=end))
    return [article.headline for article in news_set.data.get("news", [])]


class MLTrader(Strategy):
    def initialize(self, symbol: str = "SPY", cash_at_risk: float = 0.05, news_client=None):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.news_client = news_client

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = position_size(cash, last_price, self.cash_at_risk)
        return cash, last_price, quantity

    def get_sentiment(self):
        today = self.get_datetime()
        headlines = fetch_headlines(
            self.news_client, self.symbol, today - timedelta(days=NEWS_LOOKBACK_DAYS), today
        )
        return estimate_sentiment(headlines)

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment()
        signal = decide(sentiment, probability, cash, last_price, quantity, self.last_trade)
        if signal is None:
            return
        if signal.close_existing:
            self.sell_all()
        order = self.create_order(
            self.symbol,
            signal.quantity,
            signal.side,
            type="bracket",
            take_profit_price=signal.take_profit_price,
            stop_loss_price=signal.stop_loss_price,
        )
        self.submit_order(order)
        self.last_trade = signal.side


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backtest the sentiment strategy (simulation only).")
    parser.add_argument("--symbol", default="SPY")
    parser.add_argument("--cash-at-risk", type=float, default=0.05)
    parser.add_argument("--start", default="2025-04-02", help="YYYY-MM-DD")
    parser.add_argument("--end", default="2026-03-31", help="YYYY-MM-DD")
    args = parser.parse_args(argv)
    args.start = datetime.strptime(args.start, "%Y-%m-%d")
    args.end = datetime.strptime(args.end, "%Y-%m-%d")
    if args.end <= args.start:
        parser.error("--end must be after --start")
    if not 0 < args.cash_at_risk <= 1:
        parser.error("--cash-at-risk must be in (0, 1]")
    return args


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    creds = load_credentials()
    MLTrader.backtest(
        YahooDataBacktesting,
        args.start,
        args.end,
        parameters={
            "symbol": args.symbol,
            "cash_at_risk": args.cash_at_risk,
            "news_client": make_news_client(creds),
        },
    )


if __name__ == "__main__":
    main()
