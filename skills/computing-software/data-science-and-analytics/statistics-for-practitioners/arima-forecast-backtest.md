---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.arima-forecast-backtest
name: arima-forecast-backtest
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [arima-forecast, exponential-smoothing, rolling-origin-backtest]
level: advanced
status: draft
description: "Fit ARIMA or exponential smoothing in statsmodels and judge forecasts by rolling-origin backtests against a naive baseline."
sources:
  - https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Forecasting
```python
from statsmodels.tsa.arima.model import ARIMA
m = ARIMA(y, order=(1,1,1), seasonal_order=(1,1,1,12)).fit()
f = m.get_forecast(12); f.predicted_mean; f.conf_int()
```
Backtest: expand the training window step by step, forecast h steps, compare MAE with a seasonal-naive forecast.
## Gotchas
- Always beat a naive baseline or the model adds nothing.
- Intervals assume the model is right; they are optimistic.
- Never evaluate on shuffled splits.
## Verify
- [ ] Backtest MAE reported against the naive baseline.
