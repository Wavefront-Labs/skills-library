---
id: business-finance.risk-management.financial-risk-modelling.historical-var-and-backtesting
name: historical-var-and-backtesting
category: business-finance
field: risk-management
product: financial-risk-modelling
tags: [financial-risk-modelling, risk-management, market-risk, value-at-risk, var, historical-simulation, parametric-var, monte-carlo-var, expected-shortfall, es, cvar, backtesting, kupiec-test, traffic-light-test, basel, frtb, stressed-var, stress-testing, scenario-analysis, risk-factors, full-revaluation, model-validation, python, numpy, pandas]
level: advanced
status: gated
description: "Compute 1-day 99% historical-simulation VaR and expected shortfall for a portfolio, scale it carefully, backtest exceptions with the Basel traffic-light zones, and know where VaR misleads."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Historical VaR and backtesting — measure market risk and check the measure

**Goal:** estimate how much a portfolio could lose over a short horizon at a stated
confidence, check against actual P&L whether the model is right, and report its blind
spots alongside the number.

## 1. Definitions
- **VaR(99%, 1 day)** — the loss that should be exceeded on only ~1% of days. It says
  nothing about how bad those days are.
- **Expected shortfall (ES)** — the average loss on the days beyond VaR. Basel's FRTB
  replaced VaR with **97.5% ES** for regulatory market-risk capital under internal models (gated: unconfirmed, source is paywalled or blocked).
- Methods: **parametric** (variance–covariance, assumes normality — understates fat tails),
  **historical simulation** (replays actual past moves; no distribution assumption),
  **Monte Carlo** (simulated factor moves; flexible, model-dependent).

## 2. Historical simulation step by step
1. Choose risk factors (prices, rates by tenor, FX, vol surfaces, spreads) and a lookback
   window — commonly **250–500 trading days**; regulatory minimum for internal-model VaR
   was one year (gated: unconfirmed, source is paywalled or blocked).
2. Compute daily factor changes: **relative (returns)** for prices/FX, **absolute** for rates
   and spreads (relative changes misbehave near zero or negative rates).
3. Apply each historical day's changes to **today's** portfolio — full revaluation for
   options and non-linear instruments; sensitivities (delta/gamma) only as an approximation.
4. You now have N hypothetical P&Ls. VaR = the loss at the 1st percentile; ES = mean of the
   losses beyond it.

```python
import numpy as np
pnl = np.asarray(hypothetical_pnl)          # one value per historical scenario, today's portfolio
var99 = -np.percentile(pnl, 1)               # positive number = loss
es975 = -pnl[pnl <= np.percentile(pnl, 2.5)].mean()
```
With 250 scenarios the 1% tail is only 2–3 points: the estimate is noisy. State it. (Run on 250 N(0,1) draws: 3 scenarios at or below the 1st percentile, 7 at or below the 2.5th; `np.percentile` interpolates between order statistics. The 97.5% ES (2.31) came out below the 99% VaR (2.36) in that sample, because they use different tails, so do not compare them directly.)

## 3. Horizon scaling
√t scaling (10-day VaR ≈ 1-day VaR × √10) assumes independent, identically distributed
returns and a static portfolio. It's a convention, not a truth — autocorrelation and
volatility clustering break it. Prefer overlapping multi-day returns or disclose the convention.

## 4. Backtesting
Compare each day's VaR with the next day's P&L; a loss larger than VaR is an **exception**.
- Use **hypothetical P&L** (today's positions, next day's prices — no intraday trading, no
  fees) for a clean model test, and also **actual P&L** for a business view.
- At 99% over 250 days you expect 2.5 exceptions (computed; the chance of 10 or more is 0.025% under a correct model, binomial n=250, p=0.01). Basel's **traffic-light** zones: **green
  0–4**, **yellow 5–9**, **red 10+** exceptions (gated: unconfirmed, source is paywalled or blocked). A Kupiec likelihood-ratio test on 5, 9 and 10 exceptions gives p = 0.16, 0.0014 and 0.0003 (computed).
- **Kupiec (proportion-of-failures) test** checks the exception rate statistically;
  **Christoffersen** adds whether exceptions cluster (they shouldn't).
- Investigate every exception: model gap (missing factor, proxy), data issue, or genuine tail event.

## 5. Stress testing alongside VaR
VaR uses a window of history that may contain no crisis. Add:
- **Stressed VaR** — same method on a 12-month period of significant stress for the portfolio.
- **Historical scenarios** (2008, March 2020, 2022 rates shock) and **hypothetical** ones
  tailored to concentrations (a 200 bp curve twist, a 30% fall in the largest single exposure).
- Reverse stress tests: what move would cause a loss that breaks a limit or capital?

## 6. Model validation
An independent validator checks conceptual soundness, data, factor coverage, proxies,
implementation (re-code the calculation), backtests and limitations. Document assumptions
and known weaknesses — model risk management guidance (e.g. US SR 11-7) expects it (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Missing risk factors (basis between a hedge and its underlying, vol skew) make VaR look small.
- Proxies for illiquid instruments hide idiosyncratic risk.
- A calm lookback window understates risk just before volatility returns — VaR is procyclical.
- Aggregating desk VaRs by adding them ignores diversification; using full portfolio VaR
  ignores that diversification can disappear in a crisis.
- Option positions on sensitivity approximations can be badly off for large moves.

## Verify
- [ ] Factors, window, return type (relative/absolute) and revaluation method documented.
- [ ] VaR and ES reported with confidence, horizon and scenario count.
- [ ] Backtest exception count and zone reported; each exception explained.
- [ ] Stressed VaR and named stress scenarios run alongside.
- [ ] Known limitations and proxies listed for the validation file.

Related: business-finance.risk-management.credit-risk-management.
