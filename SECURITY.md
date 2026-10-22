# Security Policy

## Reporting a vulnerability
Report privately via https://github.com/hellpuffyt/ml-tradingbot/security/advisories/new — please do not open a public issue.

## Credentials
- Alpaca keys are read only from the environment (`ALPACA_API_KEY`, `ALPACA_API_SECRET`). Never commit them.
- **Known incident:** an early commit of this repository contained Alpaca API credentials in `tradingbot.py`
  (removed in a later commit, still present in git history). Those credentials must be considered compromised and
  revoked/rotated in the Alpaca dashboard. Rewriting history does not un-leak a published key.

## Trading safety
This project only runs simulated backtests. There is no live-trading code path; the program refuses to start when
`ALPACA_PAPER` is false. Changes that add order routing to a real broker are out of scope.
