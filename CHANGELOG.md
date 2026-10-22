# Changelog

All notable changes to this project are documented here (format: Keep a Changelog).

## [Unreleased]
### Security
- Credentials are read only from environment variables; a live-trading request (`ALPACA_PAPER=false`) is refused. Removed the unused `config_template.py`, which suggested switching to the live endpoint.
- Importing `tradingbot.py` no longer constructs an Alpaca broker and runs a backtest as a side effect.
### Fixed
- `requirements.txt` could not be installed: `alpaca-trade-api==4.12.0` and `quantstats-lumi==0.0.59` do not exist, `lumibot==4.4.58` conflicts with `quantstats-lumi==0.0.59`, and torch/numpy/pandas pins had no wheels for the advertised Python 3.13. Replaced with a fully pinned, generated lock (`requirements.in` → `requirements.txt`, Python 3.12): with only top-level pins, `pip` backtracked for over 30 minutes in a clean clone; the pinned file installs in ~2.5 minutes.
- News fetching moved from the deprecated `alpaca-trade-api` (incompatible with current LumiBot/yfinance) to `alpaca-py`'s `NewsClient`.
- A negative-sentiment short could only trigger when cash was *below* the share price (mis-nested `elif`).
- Flipping from a short to a long never closed the short (`"Sell"` vs `"sell"`).
- Position sizing bought one share even when `cash_at_risk` of cash was less than the share price.
- FinBERT is loaded lazily, runs under `no_grad`, truncates long inputs and returns a plain float.
### Added
- Tests, CI, `.env.example`, `SECURITY.md`, `.editorconfig`, `docs/PRODUCTION_READINESS.md`, command-line options for symbol/dates/cash-at-risk.
### Changed
- README/QUICKSTART: prominent risk disclaimer; removed the unverified "example" backtest results (+15 %, Sharpe 1.45) and the "Production Ready" status; documented that only backtesting is implemented; credited the tutorial project this is based on.
