# ML Trading Bot Configuration Template
# Copy this file to config.py and fill in your actual values
# DO NOT commit config.py to version control!

# ============================================
# ALPACA TRADING API CREDENTIALS
# ============================================
# Get these from https://app.alpaca.markets
API_KEY = "YOUR_ALPACA_API_KEY_HERE"
API_SECRET = "YOUR_ALPACA_SECRET_KEY_HERE"

# Paper trading endpoint (for testing)
# https://paper-api.alpaca.markets
# 
# Live trading endpoint (for production)
# https://api.alpaca.markets
BASE_URL = "https://paper-api.alpaca.markets"

# Paper trading flag - set to False for live trading
PAPER_TRADING = True

# ============================================
# STRATEGY PARAMETERS
# ============================================
TRADING_SYMBOL = "SPY"          # Stock ticker to trade
CASH_AT_RISK = 0.05             # Risk 5% of total capital per trade (0.05 = 5%)
SLEEP_TIME = "24H"              # Sleep between trading iterations

# ============================================
# SENTIMENT ANALYSIS SETTINGS
# ============================================
POSITIVE_THRESHOLD = 0.999      # Confidence threshold for positive sentiment (0.0-1.0)
NEGATIVE_THRESHOLD = 0.999      # Confidence threshold for negative sentiment (0.0-1.0)
NEWS_LOOKBACK_DAYS = 3          # How many days back to fetch news

# ============================================
# RISK MANAGEMENT
# ============================================
TAKE_PROFIT_PERCENT = 1.20      # Sell at 20% profit (1.20x entry price)
STOP_LOSS_PERCENT = 0.95        # Exit at 5% loss (0.95x entry price)

# ============================================
# BACKTESTING PARAMETERS
# ============================================
BACKTEST_START_DATE = "2025-04-02"   # YYYY-MM-DD format
BACKTEST_END_DATE = "2026-03-31"     # YYYY-MM-DD format

# ============================================
# ML MODEL SETTINGS
# ============================================
FINBERT_MODEL = "ProsusAI/finbert"   # HuggingFace model ID
USE_GPU = True                        # Use GPU if available (CUDA)

# ============================================
# LOGGING & DEBUGGING
# ============================================
DEBUG_MODE = False                    # Enable verbose logging
LOG_FILE = "trading_bot.log"          # Log file path
