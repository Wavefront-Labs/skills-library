---
id: computing-software.ai-ml-engineering.scikit-learn.quantile-regression-quantileregressor
name: quantile-regression-quantileregressor
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, quantileregressor, quantile-regression, prediction-intervals, pinball-loss, gradient-boosting-quantile]
level: practitioner
status: verified
description: "Predict conditional quantiles and intervals: QuantileRegressor (linear, highs solver, alpha), GradientBoosting/HistGB quantile loss, pinball scoring and crossing quantiles."
sources:
  - https://scikit-learn.org/stable/modules/linear_model.html#quantile-regression
  - https://scikit-learn.org/stable/auto_examples/linear_model/plot_quantile_regression.html
  - https://scikit-learn.org/stable/auto_examples/ensemble/plot_gradient_boosting_quantile.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Quantile regression

**Use when:** you need a prediction interval or a specific quantile (e.g. stock to hold at the 90th percentile of demand), or errors are heteroscedastic.

## Linear: QuantileRegressor
```python
from sklearn.linear_model import QuantileRegressor
q90 = QuantileRegressor(quantile=0.9, alpha=0.0, solver="highs").fit(X, y)
```
- Minimizes pinball loss with an L1 penalty `alpha` (the default is `alpha=1.0`, so set 0 for no regularization; scale features first when alpha > 0). On simulated heteroscedastic data `alpha=0` at `quantile=0.9` covered 90.8% of 1,000 held-out points.
- `solver="highs"` (linear programming) is the default; fitting 20,000 rows x 5 features took 9.4 s here and the cost grows quickly with n_samples, so for large data subsample or use boosting.

## Non-linear: gradient boosting
```python
from sklearn.ensemble import HistGradientBoostingRegressor
models = {q: HistGradientBoostingRegressor(loss="quantile", quantile=q, max_iter=500).fit(X, y)
          for q in (0.05, 0.5, 0.95)}
lo, med, hi = (models[q].predict(X_test) for q in (0.05, 0.5, 0.95))
```
LightGBM (`objective="quantile", alpha=q`) and XGBoost (`objective="reg:quantileerror", quantile_alpha=np.array([0.05, 0.5, 0.95])`, multi-quantile in one model: `predict` returned shape `(n, 3)`) work the same way (all ran; held-out coverage with default settings was 0.848 for LightGBM at q=0.9 and 0.094/0.488/0.897 for the three XGBoost quantiles).

## Scoring
- `mean_pinball_loss(y, pred, alpha=q)`; scorer via `make_scorer(mean_pinball_loss, alpha=q, greater_is_better=False)` for tuning each quantile model separately.
- Check coverage: fraction of y within [lo, hi] should be close to 0.90 on held-out data. With `max_iter=500` the HistGradientBoosting 5%/95% pair covered 89% of the training rows but only 74.5% of held-out rows, so the snippet above needs regularisation (fewer iterations, `min_samples_leaf`, early stopping) before the interval is trustworthy.

## Pitfalls
- **Quantile crossing:** independently fit models can give lo > hi for some x (no crossings occurred in the simulated test, so check yours). Sort predictions per row, or use a joint model (XGBoost multi-quantile, or conformalized quantile regression).
- Coverage on training data is optimistic; validate on held-out data and consider conformal calibration (CQR) for guaranteed marginal coverage.
- Extreme quantiles (0.01/0.99) need lots of data; estimates are noisy.

## Verify
- [ ] Empirical coverage and mean interval width reported on a test set, per important segment.
