# Production readiness — ml-tradingbot

Audit date: 2026-10-22. Treated as financial software: nothing was run against a real brokerage, with real money,
or with real API keys.

## Scope
Educational sentiment strategy: FinBERT scores Alpaca historical news headlines; `signals.decide()` maps sentiment to
bracket orders; LumiBot runs a **simulated backtest** on Yahoo Finance prices. There is no live- or paper-trading
runtime path (the README previously implied one). Based on nicknochnack/MLTradingBot.

Modules: `signals.py` (pure logic + env credentials), `finbert_utils.py` (lazy FinBERT), `tradingbot.py`
(LumiBot strategy + CLI, backtest only).

## Safety properties (verified)
| Property | How verified |
|---|---|
| No live-trading endpoint in code | `tests/test_safety.py::test_no_live_trading_endpoint_in_code` |
| No broker/live trader constructed; import has no side effects | `test_no_live_trader_or_broker_is_constructed`, `tests/test_tradingbot.py` imports the module |
| Keys only from env; none in source | `test_credentials_come_from_environment_and_are_paper_only`, `test_no_credentials_assigned_in_source` |
| Missing keys → exit 1 before any network/backtest | `test_main_refuses_without_credentials`; manual run (exit 1) |
| `ALPACA_PAPER=false` refused | `test_live_trading_request_is_refused`; manual run |
| Orders only in LumiBot's backtesting broker | code review: the only entry point is `MLTrader.backtest(YahooDataBacktesting, ...)` |
| Prominent risk disclaimer, no return claims | README top section; fabricated "example" results removed |

## Platforms and prerequisites
Python 3.12 (macOS arm64 verified locally; Ubuntu via CI definition). Python 3.13 resolves with the same pins
(`uv pip compile --python-version 3.13`) but was not run. A real backtest needs free Alpaca paper keys (news data)
and network access to Yahoo Finance and Hugging Face; FinBERT is ~438 MB.

## Clean-clone commands
See README "Quick start" / "Testing". Results are recorded below.

## Commands executed and outcomes
| Command | Exit | Result |
|---|---|---|
| baseline `uv pip install --dry-run -r requirements.txt` (Py 3.13) | 1 | unsatisfiable: lumibot==4.4.58 needs quantstats-lumi>=1.1.3, file pins 0.0.59; `alpaca-trade-api==4.12.0` does not exist on PyPI (latest 3.2.0) |
| `alpaca-trade-api` 3.2.0 + current lumibot | 1 | incompatible (websockets<11 vs yfinance>=13) → moved news to `alpaca-py` |
| baseline tests | — | none existed |
| `python -m pytest` (after fixes) | 0 | 32 passed, 0 failed, 0 skipped |
| `python tradingbot.py` without keys | 1 | clear message, no network or backtest |
| `ALPACA_PAPER=false python tradingbot.py` | 1 | refuses live trading |
| **stand-in** backtest: real LumiBot 4.6.24 + Yahoo prices, Mar 2025, **stub news + stub sentiment (always positive 0.9999)** | 0 | completed; 23 simulated fills of SPY bracket buys (first: 8 shares at 596.18 = ~5 % of 100k). Verifies wiring only; the numbers are meaningless as strategy results and are deliberately not reported as performance |
| `uvx pip-audit` on the installed env | 1 | certifi 2025.11.12 (fixed in 2026.10.19; a fresh install resolves the fixed version), setuptools 80.10.2 (fix 83.0.0, but lumibot 4.6.24 requires setuptools<81) |
| history secret scan | — | **HIT** (see security) |

## Tests
- Unit: `test_signals.py` (decision table, flips, thresholds, sizing, credentials, live refusal), `test_safety.py`.
- Wiring: `test_tradingbot.py` calls `MLTrader.on_trading_iteration` on a stub with fake broker methods (no LumiBot
  runtime, no orders), `fetch_headlines` with a fake client, CLI validation, no-credential refusal.
- Model path: `test_finbert_pipeline.py` uses a **tiny random stand-in model**, not FinBERT; checks shapes/types/
  truncation and that importing does not load torch/transformers.

## CI
`.github/workflows/ci.yml`: Ubuntu, Python 3.12, CPU torch, pytest; actions pinned to SHAs resolved via the GitHub
API (checkout v7.0.1, setup-python v7.1.0); `contents: read`; no secrets. Default branch: no workflow (never run);
audit branch: pending until pushed.

## Bugs fixed
1. Uninstallable requirements (non-existent versions, conflicts, no wheels for the advertised Python).
2. Deprecated, incompatible `alpaca-trade-api` → `alpaca-py` NewsClient.
3. Short entry only when cash < price (mis-nested `elif`) — `test_negative_sentiment_shorts_when_cash_is_available`.
4. Short never closed on flip (`"Sell"` vs `"sell"`) — `test_flip_from_short_to_long_closes_the_short_first`.
5. Position sizing exceeded the risk budget (`max(1, …)`) — `test_position_size_never_exceeds_cash_at_risk`.
6. Import side effects: broker construction + backtest at import; FinBERT loaded at import — `test_tradingbot.py`, `test_import_does_not_load_finbert`.
7. Hard-coded credential constants → environment only — `tests/test_safety.py`.

## Security findings
- **HIGH — leaked credentials in history:** commits 0be77cb and cfb4f98 contain an Alpaca API key ID (paper-key
  prefix) and secret in `tradingbot.py` lines 8–9; removed from the tree in ac9faa9. Not printed here. They must be
  **revoked/rotated** in Alpaca. History was not rewritten (not this audit's call; rotation is the real fix).
- Provenance/licensing: code derives from nicknochnack/MLTradingBot, which has **no license**; this repo ships MIT
  under "ML Trading Bot Contributors". Commit authors are "Prabesh Sharma" and "Trading Bot Dev". Owner should confirm
  the right to relicense.
- Dependency advisories as listed above.

## Known limitations / unverified
- Real backtest with real FinBERT and real Alpaca news **not run** (no keys; FinBERT not downloaded per audit rules).
- Strategy quality is unknown; no performance numbers are published.
- Python 3.13 not executed.

## Acceptance checklist
| # | Item | Expected | Command/test | Result | Actual | Reference |
|---|---|---|---|---|---|---|
| 1 | Install | succeeds | `pip install -r requirements.txt` | pass | clean clone exit 0 | requirements.txt |
| 2 | Safe default | no live path, refuses `ALPACA_PAPER=false` | test_safety, test_signals | pass | — | signals.py |
| 3 | Keys from env only | missing → exit 1 | manual + test | pass | exit 1 | signals.load_credentials |
| 4 | Decision table matches README | buy/short/hold | test_signals | pass | — | signals.decide |
| 5 | Order wiring | bracket order, flip closes | test_tradingbot | pass | — | tradingbot.MLTrader |
| 6 | Sentiment code path | float prob + label | test_finbert_pipeline (stand-in) | pass | — | finbert_utils |
| 7 | Backtest runs in LumiBot | completes | stand-in backtest | pass (stub sentiment/news) | 23 fills | this file |
| 8 | Real FinBERT + Alpaca news backtest | completes | `python tradingbot.py` with keys | not run | no keys | — |
| 9 | No return claims | none | README review | pass | removed | README |
| 10 | No secrets in tree | none | regex scan | pass (tree) / **fail (history)** | rotation needed | SECURITY.md |

## Classification proposal
**Partially Verified** — safety properties, logic and LumiBot wiring are tested; the real end-to-end backtest
(FinBERT + Alpaca news) could not be run without keys, and leaked keys in history need rotation.

## Tested commit
Branch `audit/production-readiness`, commit adding this file (code at d5047f7), 2026-10-22.
