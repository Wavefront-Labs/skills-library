---
id: computing-software.ai-ml-engineering.model-training.forecast-metrics-mase-wape
name: forecast-metrics-mase-wape
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, mase, wape, smape, forecast-evaluation, time-series, metrics]
level: practitioner
status: gated
description: "Evaluate forecasts with the right metric: MAE/RMSE scale issues, MAPE failure on zeros, sMAPE, WAPE for aggregate accuracy, MASE vs naive baselines, and backtest evaluation."
sources:
  - https://otexts.com/fpp3/accuracy.html
  - https://robjhyndman.com/papers/mase.pdf
  - https://otexts.com/fpp3/tscv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Forecast metrics (MASE, sMAPE, WAPE)

## Metric guide
| Metric | Formula (sketch) | Use / caveat |
|---|---|---|
| MAE | mean abs(y - f) | same units as data; can't compare across series |
| RMSE | sqrt(mean (y - f)^2) | penalizes large errors; targets the mean |
| MAPE | mean abs(y - f) / abs(y) | undefined at y=0, explodes near 0, asymmetric (FPP3: heavier penalty on negative errors y - f, i.e. over-forecasts) |
| sMAPE | mean 2 abs(y - f) / (abs(y) + abs(f)) | the abs() form is bounded in [0, 2], but FPP3's form `200|y-f|/(y+f)` can be negative, is unstable near 0 and Hyndman and Koehler recommend against it; state your definition |
| WAPE | sum abs(y - f) / sum abs(y) | volume-weighted; robust for intermittent retail demand; business-friendly |
| MASE | MAE / in-sample MAE of the (seasonal) naive forecast on the training data | scale-free, works with zeros; < 1 means smaller than the in-sample one-step naive error (FPP3), which is not the same as beating naive out of sample |
| Pinball / CRPS | quantile / distribution scores | probabilistic forecasts |

## MASE
```python
import numpy as np
def mase(y_train, y_true, y_pred, m=1):        # m = seasonal period (7 daily-weekly, 12 monthly); y_* are numpy arrays (formula matches FPP3 and ran)
    scale = np.mean(np.abs(y_train[m:] - y_train[:-m]))
    return np.mean(np.abs(y_true - y_pred)) / scale
```
Report against seasonal naive explicitly; many sophisticated forecasts barely beat it.

## Aggregating across many series
- WAPE across all SKUs weights by volume (big sellers dominate); MASE averaged across series weights series equally. Report both, or weight by revenue if that is the business objective.
- Never average MAPE over series with near-zero volumes.

## Evaluation protocol
Rolling-origin backtesting (time series CV): multiple forecast origins, fixed horizon, metrics per horizon step (error grows with horizon). Libraries: sktime, `statsforecast` (`cross_validation`) and Darts (`historical_forecasts`) provide rolling-origin evaluation (names from memory, packages not installed here (gated: unconfirmed, source is paywalled or blocked)).

## Bias
Track mean error / forecast bias separately (`sum(f - y) / sum(y)`); accuracy metrics can look fine while the forecast systematically over-orders.

## Verify
- [ ] Backtest table: model vs seasonal naive, by horizon, with WAPE, MASE and bias.
