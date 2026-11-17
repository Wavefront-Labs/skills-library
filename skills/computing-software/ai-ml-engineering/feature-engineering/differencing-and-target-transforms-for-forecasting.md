---
id: computing-software.ai-ml-engineering.feature-engineering.differencing-and-target-transforms-for-forecasting
name: differencing-and-target-transforms-for-forecasting
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, time-series, differencing, stationarity, detrending, target-transform, forecasting]
level: practitioner
status: verified
description: "Apply differencing, seasonal differencing and log transforms to forecasting targets, reconstruct forecasts, test stationarity, and let tree models handle trends."
sources:
  - https://otexts.com/fpp3/stationarity.html
  - https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.adfuller.html
  - https://skforecast.org/latest/user_guides/time-series-differentiation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Differencing and target transforms for forecasting

**Goal:** make a trending or seasonal series learnable, especially for ML models that can't extrapolate.

## Why
- Tree-based models (GBMs, random forests) predict within the range of training targets; with an upward trend, they forecast a flat line at the last seen level.
- Many statistical models assume stationarity (constant mean/variance).
Modelling changes instead of levels fixes both.

## Transforms
- **First difference:** `y'_t = y_t - y_{t-1}` removes a linear trend.
- **Seasonal difference:** `y'_t = y_t - y_{t-m}` (m = 7 daily-weekly, 12 monthly-yearly) removes stable seasonality.
- **Log then difference:** `log(y_t) - log(y_{t-1})` ~ growth rate; stabilises variance that grows with level (use `log1p` with zeros).
- **Ratio to a rolling mean / normalisation per series** for global models across many series of different scales.

```python
s = np.log1p(series)
d = s.diff().dropna()
# model predicts d_hat for steps h = 1..H
level = s.iloc[-1] + np.cumsum(d_hat)          # reconstruct
forecast = np.expm1(level)
```
skforecast exposes a `differentiation` parameter in its forecasters and reverses it at prediction; sktime has a `Differencer` transformer (`sktime.transformations.difference`).

## Testing stationarity
```python
from statsmodels.tsa.stattools import adfuller, kpss
adfuller(series.dropna())[1]   # p < 0.05 -> reject unit root (stationary-ish)
kpss(series.dropna(), regression="c")[1]   # p < 0.05 -> reject stationarity
```
Use both; they test opposite null hypotheses. On a random walk: ADF p=0.84, KPSS p=0.01 (statsmodels warns the KPSS p-value is truncated to the table range).

On a linear trend, a default `LGBMRegressor` predicted 376 at t=290 (truth 580) while `linear_tree=True` predicted 574 (checked). Over-differencing (differencing a stationary series) adds noise and negative autocorrelation.

## Gotchas
- Errors accumulate when reconstructing multi-step forecasts from predicted differences; evaluate on the level scale at each horizon.
- Lag features must be computed on the same scale as the target (differenced lags for a differenced target).
- Log transform forecasts are median-like; back-transformed sums underestimate totals (apply a bias correction if totals matter).
- Alternatively keep levels and add trend features (time index, linear model on top), or use models that extrapolate (linear trees, `LightGBM(linear_tree=True)`).

## Verify
- [ ] Backtest with rolling origin, evaluated on the original scale.
- [ ] Forecast continues the trend instead of flattening (plot it).
- [ ] Stationarity tests and the chosen differencing order documented.
