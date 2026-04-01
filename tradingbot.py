from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
from datetime import datetime, timedelta
from alpaca_trade_api.rest import REST, TimeFrame
from finbert_utils import estimate_sentiment

API_KEY = "API_KEY"
API_SECRET = "API_SECRET"
BASE_URL = "https://paper-api.alpaca.markets"

ALPACA_CREDS={
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET, 
    "PAPER": True
}

class MLTrader(Strategy):
    def initialize(self, symbol: str="SPY", cash_at_risk: float=0.05):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api_=REST(key_id=API_KEY, secret_key=API_SECRET, base_url=BASE_URL)

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = max(1, int(cash * self.cash_at_risk / last_price))
        return cash, last_price, quantity
    
    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - timedelta(days=3)
        return today.strftime("%Y-%m-%d"), three_days_prior.strftime("%Y-%m-%d")
    
    def get_sentiment(self):
        today, three_days_prior = self.get_dates()
        news = self.api_.get_news(symbol=self.symbol,
                                   start=three_days_prior,
                                   end=today)
        if news:
            news_headlines = [ev.__dict__["_raw"]["headline"] for ev in news]
            probability, sentiment = estimate_sentiment(news_headlines)
            return probability, sentiment
        else:
            return 0, "neutral"      

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment()
        if cash > last_price :
                
            if sentiment == "positive" and probability > 0.999:
                if self.last_trade == "Sell":
                    self.sell_all()
            
          
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price * 1.20,
                    stop_loss_price=last_price * 0.95,
                )
                self.submit_order(order)
                self.last_trade = "buy"




        elif sentiment == "negative" and probability > 0.999:
                if self.last_trade == "buy":
                    self.sell_all()
            
          
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "sell",
                    type="bracket",
                    take_profit_price=last_price * 0.80,
                    stop_loss_price=last_price * 1.05,
                )
                self.submit_order(order)
                self.last_trade = "sell"

start_date = datetime(2025, 4, 2)
end_date = datetime(2026, 3, 31)
broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name="mlstrat", broker=broker,
                    parameters={"symbol": "SPY", "cash_at_risk": 0.05})

strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={"symbol": "SPY"}
)
