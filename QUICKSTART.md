# Quick Start

> Educational backtest only — no live trading, not financial advice. See the disclaimer in README.md.

1. Install (Python 3.12):
   ```bash
   git clone https://github.com/hellpuffyt/ml-tradingbot.git && cd ml-tradingbot
   python3.12 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create free Alpaca **paper** API keys at https://app.alpaca.markets and export them:
   ```bash
   export ALPACA_API_KEY=... ALPACA_API_SECRET=...
   ```
   (Do not edit them into any file; the program only reads the environment.)
3. Run a backtest:
   ```bash
   python tradingbot.py --start 2025-04-02 --end 2026-03-31
   ```
   The first run downloads FinBERT (~438 MB). Reports are written to `logs/`.

## Common issues
- `Set ALPACA_API_KEY and ALPACA_API_SECRET ...` (exit code 1) — the keys are not exported in this shell.
- `ALPACA_PAPER=false requested live trading ...` — unset `ALPACA_PAPER`; live trading is not supported.
- Slow first run / Hugging Face warnings — the model download; later runs use the cache.
