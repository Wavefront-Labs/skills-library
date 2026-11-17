---
id: mathematics.statistics.time-series-analysis.arima-forecasting-workflow
name: arima-forecasting-workflow
category: mathematics
field: statistics
product: time-series-analysis
tags: [statistics, time-series-analysis, time-series, forecasting, arima, sarima, seasonal-arima, ets, exponential-smoothing, stationarity, differencing, adf-test, kpss-test, acf, pacf, seasonal-decomposition, stl, ljung-box, backtesting, time-series-cross-validation, mase, mape, prediction-intervals, statsmodels, fable, forecast-package, auto-arima]
level: practitioner
status: gated
description: "Forecast a series with ARIMA/ETS: plot and decompose, make it stationary, identify orders from ACF/PACF, check residuals, backtest against naive baselines, report intervals."
sources:
  - https://otexts.com/fpp3/diagnostics.html
  - https://otexts.com/fpp3/accuracy.html
  - https://otexts.com/fpp3/stationarity.html
  - https://www.statsmodels.org/stable/tsa.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ARIMA forecasting workflow

**Goal:** produce a forecast with honest prediction intervals that demonstrably beats
a naive baseline on held-out data.

## 1. Look before modelling
- Plot the series at full resolution and fix the **frequency** (daily, weekly, monthly).
  Fill or flag gaps explicitly; ARIMA assumes regular spacing.
- **STL decomposition** (R `stl()`, Python `statsmodels.tsa.seasonal.STL`) to see
  trend, seasonality and remainder. Note level shifts, outliers, calendar effects
  (Easter, trading days).
- If variance grows with level, use **log** (or Box-Cox) and back-transform forecasts.
  Back-transformed log forecasts are medians, not means — say so or bias-adjust.

## 2. Always build baselines first
- **Naive** (last value), **seasonal naive** (value one season ago), **drift**.
Every candidate model must beat these on backtests. Surprisingly often it doesn't.

## 3. Stationarity and differencing
ARIMA(p, d, q) models a stationary series after d differences.
- Use **KPSS** (H0: stationary) and **ADF** (H0: unit root) together; `pmdarima.ndiffs()`
  or R `forecast::ndiffs()` automate it.
- Seasonal differencing (D = 1, lag 12 for monthly) first if seasonality is strong;
  rarely need d + D > 2 (gated: unconfirmed, source is paywalled or blocked). Over-differencing shows as a strong negative lag-1 ACF (near −0.5).

## 4. Identify orders from ACF/PACF (or search)
On the differenced series:
- PACF cuts off after lag p, ACF tails off → **AR(p)**.
- ACF cuts off after lag q, PACF tails off → **MA(q)**.
- Both tail off → mixed ARMA; let AICc choose.
Seasonal analogues appear at multiples of the season lag. In practice, use an automated
search (`forecast::auto.arima`, `fable::ARIMA()`, `pmdarima.auto_arima(seasonal=True, m=12)`)
and sanity-check the chosen orders against the plots. Compare models **only with the
same d** by AIC/AICc (differencing changes the likelihood's data).

## 5. Also try ETS
Exponential smoothing state-space models (`forecast::ets`, `fable::ETS`,
`statsmodels ExponentialSmoothing`) handle trend/seasonality directly and are often
as accurate as ARIMA. Damped-trend ETS is a robust default for long horizons.

## 6. Residual diagnostics
Residuals should look like white noise:
- ACF of residuals within bounds; **Ljung-Box** test p > 0.05 at lag 10 (non-seasonal)
  or 2m (seasonal, m = period), capped at T/5 (fpp3 recommendation). R `checkresiduals(fit)`; Python `acorr_ljungbox`.
- No remaining seasonality, roughly constant variance. Non-normal residuals mainly
  affect interval width — consider bootstrapped intervals.

## 7. Backtest properly
Use **rolling-origin (time-series) cross-validation**: fit on data up to t, forecast
h steps, roll forward. Never shuffle; never use future information in features.
Score with **MASE** (scale-free; errors are scaled by the in-sample MAE of the naive, or seasonal-naive, method, so < 1 means better than that in-sample baseline; also compare against naive baselines on the same test window) and RMSE.
Avoid MAPE when values approach zero — it explodes and is asymmetric.

## 8. Report
Forecast with **80% and 95% prediction intervals**, the model spec, backtest MASE vs
baselines, and the date of the last observation. Intervals widen with horizon; if they
don't, something's wrong.

## Gotchas
- Fitting on the whole series and reporting in-sample error flatters every model.
- Structural breaks (COVID-era demand, a policy change) wreck ARIMA; model the break
  with a dummy or start after it.
- Multiple seasonalities (hourly data with daily + weekly cycles) need TBATS, Fourier
  regressors or Prophet-style models, not plain SARIMA.
- Uncertain: the p > 0.05 cut-off is a convention, not a standard.

## Verify
- [ ] Series plotted, frequency set, gaps and outliers handled.
- [ ] Naive and seasonal-naive baselines computed.
- [ ] Differencing justified by tests and plots; no over-differencing.
- [ ] Residuals pass Ljung-Box and show no structure.
- [ ] Rolling-origin backtest: chosen model's MASE beats baselines.
- [ ] Forecast delivered with prediction intervals and back-transform noted.
