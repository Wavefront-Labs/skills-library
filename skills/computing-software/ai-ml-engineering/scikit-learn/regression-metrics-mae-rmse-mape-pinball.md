---
id: computing-software.ai-ml-engineering.scikit-learn.regression-metrics-mae-rmse-mape-pinball
name: regression-metrics-mae-rmse-mape-pinball
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, regression-metrics, pinball-loss, mape, rmse, r2-score]
level: practitioner
status: verified
description: "Pick and compute regression metrics in scikit-learn: MAE, RMSE, MAPE, R2, median and pinball loss for quantiles, and which loss each metric's optimal prediction targets."
sources:
  - https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_pinball_loss.html
  - https://scikit-learn.org/stable/auto_examples/ensemble/plot_gradient_boosting_quantile.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regression metrics

The metric decides which prediction is "best": train with a matching loss.

| Metric | sklearn | Optimal point prediction | Notes |
|---|---|---|---|
| MSE / RMSE | `mean_squared_error`, `root_mean_squared_error` | conditional mean | punishes large errors; RMSE in target units |
| MAE | `mean_absolute_error` | conditional median | robust to outliers |
| MedAE | `median_absolute_error` | | robust summary, not differentiable |
| MAPE | `mean_absolute_percentage_error` | biased low (favours under-prediction) | explodes near y=0 (y=0, pred=1 gave 4.5e15); returns a fraction, not % (0.5 for 100 vs 50 or 150) |
| R2 | `r2_score` | mean | relative to predicting the mean; can be negative; not comparable across datasets |
| Pinball (quantile) | `mean_pinball_loss(alpha=q)` | conditional q-quantile | for prediction intervals |
| Poisson / Gamma / Tweedie deviance | `mean_poisson_deviance`, ... | mean under that distribution | counts, positive skewed |
| D2 scores | `d2_absolute_error_score`, `d2_pinball_score` | | R2-like generalisations |

## Quantile models and intervals
```python
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_pinball_loss
models = {q: HistGradientBoostingRegressor(loss="quantile", quantile=q).fit(X_tr, y_tr) for q in (0.05, 0.5, 0.95)}
for q, m in models.items():
    print(q, mean_pinball_loss(y_te, m.predict(X_te), alpha=q))
lo, hi = models[0.05].predict(X_te), models[0.95].predict(X_te)
print("coverage", ((y_te >= lo) & (y_te <= hi)).mean())        # should be ~0.90
```
Check empirical coverage and interval width; pinball alone doesn't guarantee calibrated intervals. In a test (500 boosting iterations, default regularisation) the 5%-95% interval covered only 74.5% of held-out points, not 90%. Conformal prediction adds marginal coverage guarantees (a method, not run here).

## Choosing
- Business cost linear in error: MAE. Large errors disproportionately bad: RMSE.
- Relative error across scales (sales of many products): avoid plain MAPE when values approach 0; use WAPE (sum|e| / sum|y|), sMAPE, or RMSLE (`root_mean_squared_log_error`) for multiplicative errors.
- Forecasting: compare to a naive baseline (MASE = MAE / MAE of seasonal naive).
- Always report a baseline (`DummyRegressor(strategy="mean"/"median")`) alongside.

## Scorer names
`neg_mean_absolute_error`, `neg_root_mean_squared_error`, `neg_mean_absolute_percentage_error`, `neg_root_mean_squared_log_error`, `r2` are built in (checked against `get_scorer_names()`); `neg_mean_pinball_loss` is not (absent from the list): use `make_scorer(mean_pinball_loss, alpha=0.9, greater_is_better=False)`.

## Gotchas
- Training with MSE then reporting MAE optimises the mean but is judged on the median; with skewed targets the gap is large.
- Log-transformed targets: back-transforming `exp(pred)` gives roughly the median, not the mean (lognormal sample: mean 1.60, median 1.01, mean of `exp(pred)` 0.99; a smearing correction is needed for the mean).
- Multi-output: `multioutput="raw_values"` to see each target (returns one value per column, e.g. `[275.06 275.06]` for two identical targets).

## Verify
Compute metrics for the model and the dummy baseline on the same split; also slice by target range to see where errors concentrate.
