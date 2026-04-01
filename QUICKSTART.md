# Quick Start Guide

## 5 Minutes to Your First Backtest

### Step 1: Clone & Install (2 min)
```bash
git clone https://github.com/yourusername/ml-trading-bot.git
cd ml-trading-bot
pip install -r requirements.txt
```

### Step 2: Get Alpaca API Keys (2 min)
1. Visit [Alpaca Markets](https://app.alpaca.markets)
2. Sign up for a free account
3. Generate API keys from the dashboard
4. Copy them (you'll need them next)

### Step 3: Configure Credentials (1 min)
Edit `tradingbot.py` and replace:
```python
API_KEY = "YOUR_ALPACA_API_KEY"      # Paste your key here
API_SECRET = "YOUR_ALPACA_SECRET_KEY" # Paste your secret here
```

### Step 4: Run Backtest (30 seconds)
```bash
python tradingbot.py
```

You should see:
```
2026-04-02 00:55:43,988 | INFO | LumiBot v4.4.58 starting
Progress |----------|  1.56% [Elapsed: 0:00:02 ETA: 0:02:54]
Sentiment: positive, Confidence: 0.82
```

---

## What Happens Next?

The bot will:
1. 📰 **Fetch news** from the past 3 days for SPY
2. 🤖 **Analyze sentiment** using FinBERT
3. 📊 **Generate trading signals** based on sentiment analysis
4. 🎯 **Execute trades** with 20% profit targets and 5% stop losses
5. 📈 **Track performance** through the historical period

---

## Common Issues & Solutions

### ❌ "ModuleNotFoundError: No module named 'lumibot'"
**Solution**: Reinstall dependencies
```bash
pip install --upgrade -r requirements.txt
```

### ❌ "ModuleNotFoundError: No module named 'torch'"
**Solution**: Install PyTorch separately (can be large)
```bash
pip install torch torchvision torchaudio
```

### ❌ "Authentication failed"
**Solution**: Check your API keys in `tradingbot.py`
- Keys are case-sensitive
- Don't add extra spaces
- Use paper trading first (`PAPER: True`)

### ❌ "CUDA out of memory"
**Solution**: Use CPU instead (set `device = "cpu"` in `finbert_utils.py`)
```python
device = "cpu"  # Force CPU usage
```

### ❌ Slow backtest / HuggingFace warnings
**Solution**: This is normal on first run (downloads 438MB model)
- Subsequent runs will be much faster (uses cache)
- Warnings about symlinks can be ignored

---

## Next Steps

### Test with Paper Trading
Once backtesting looks good, enable paper trading:

1. Keep `PAPER: True` in credentials
2. Run during market hours (9:30 AM - 4:00 PM EST)
3. Watch real trades execute on your paper account
4. Monitor daily performance

### Optimize Your Strategy
Try different parameters:
```python
parameters={
    "symbol": "AAPL",        # Try different stocks
    "cash_at_risk": 0.10     # Increase/decrease risk
}
```

### Add More Features
- Multiple symbols
- Technical indicators (RSI, MACD)
- Different sentiment thresholds
- Time-based trading rules

---

## Stay Safe 🛡️

✅ **DO:**
- Start with paper trading
- Backtest extensively
- Risk only what you can afford to lose
- Monitor your positions daily
- Use stop losses

❌ **DON'T:**
- Commit API keys to GitHub
- Trade with 100% of your capital
- Proceed to live trading without testing
- Ignore risk management
- Leave bots running unmonitored

---

## Resources

- 🤖 **[LumiBot Docs](https://lumiwealth.com/docs/)**
- 📈 **[Alpaca API Docs](https://docs.alpaca.markets/)**
- 🧠 **[FinBERT Paper](https://arxiv.org/abs/1908.10063)**
- 💻 **[PyTorch Guide](https://pytorch.org/)**

---

## Need Help?

- GitHub Issues: [Report bugs](https://github.com/yourusername/ml-trading-bot/issues)
- Discussions: [Ask questions](https://github.com/yourusername/ml-trading-bot/discussions)
- Email: your.email@example.com

---

**Happy Trading! 🚀📈**
