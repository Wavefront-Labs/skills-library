---
id: computing-software.ai-ml-engineering.scikit-learn.transformed-target-regressor
name: transformed-target-regressor
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, transformedtargetregressor, target-transform, log-target, pipeline, regression]
level: practitioner
status: verified
description: "Model transformed regression targets with TransformedTargetRegressor: log1p and quantile transforms, inverse at predict, retransformation bias and CV usage."
sources:
  - https://scikit-learn.org/stable/modules/compose.html#transforming-target-in-regression
  - https://scikit-learn.org/stable/modules/generated/sklearn.compose.TransformedTargetRegressor.html
  - https://scikit-learn.org/stable/auto_examples/compose/plot_transformed_target.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TransformedTargetRegressor

**Goal:** fit a regressor on a transformed target (log, quantile, Box-Cox) while every predict, score and cross-validation call works in the original units.

## Usage
```python
from sklearn.compose import TransformedTargetRegressor
from sklearn.preprocessing import QuantileTransformer
import numpy as np

reg = TransformedTargetRegressor(
    regressor=make_pipeline(preprocess, Ridge(alpha=1.0)),
    func=np.log1p, inverse_func=np.expm1,          # or transformer=QuantileTransformer(output_distribution="normal")
)
scores = cross_val_score(reg, X, y, cv=5, scoring="neg_mean_absolute_error")
```
- `func`/`inverse_func` for stateless transforms; `transformer=` for fitted ones (`StandardScaler`, `QuantileTransformer`, `PowerTransformer`). Use one or the other, not both.
- `check_inverse=True` (default) samples a subset and warns if `inverse_func(func(y)) != y` ("The provided functions are not strictly inverse of each other", reproduced with `np.log1p` and `np.sqrt`); heed it - a wrong inverse silently ruins every prediction. Passing both `transformer` and `func`/`inverse_func` raises `ValueError: 'transformer' and functions 'func'/'inverse_func' cannot both be set`.
- Scoring happens on the inverse-transformed predictions, so `cross_val_score` and `GridSearchCV` report errors in original units.

## Why not transform y by hand
Manually doing `model.fit(X, np.log1p(y))` means every caller must remember to `expm1` predictions, and grid-search metrics end up in log units, which ranks models differently than the business metric does.

## Retransformation bias
Fitting MSE on `log(y)` and exponentiating gives (roughly) the **median**, not the mean, of `y|X`. Summing these predictions underestimates totals (revenue, demand): on lognormal-noise data (sigma 0.8) the predicted total was 75.5% of the actual total on a held-out split, and 102.6% after multiplying by the Duan smearing factor 1.358. Options:
- Smearing correction (Duan): multiply predictions by `mean(exp(residuals_on_log_scale))` (estimated on training residuals in the test above; use validation data if the model overfits).
- Fit a model whose loss matches the target distribution instead: `PoissonRegressor`, `TweedieRegressor`, or `HistGradientBoostingRegressor(loss="poisson")` - often better than log-transform for counts and monetary amounts.

## Accessing the fitted parts
- `reg.regressor_` is the fitted inner estimator, `reg.transformer_` the fitted transformer. Grid-search params use the `regressor__` prefix: `{"regressor__ridge__alpha": [0.1, 1, 10]}`.

## Gotchas
- `log` with zeros or negatives: `np.log` on a target containing 0 raised `ValueError: Input contains infinity`; use `log1p`, or a `PowerTransformer(method="yeo-johnson")` (handles 0 and negative values; ran).
- Quantile transform with few samples gives a stair-step inverse; set `n_quantiles <= n_samples` (scikit-learn lowers it automatically with a warning: `n_quantiles (1000) is greater than the total number of samples (100)`).
- Target transforms matter most for linear models and neural nets; trees split on order, but the loss still sees the target scale: `HistGradientBoostingRegressor` MAE was 3.41 raw and 3.09 with a log target on the skewed test data, so measure rather than assume. Ridge MAE (original units, 5-fold) was 2.91 with `log1p`, 2.87 with `QuantileTransformer` and 2.87 with `PowerTransformer` on the same data.

## Verify
- [ ] Predictions are in original units (spot-check against `y`).
- [ ] No inverse-check warning.
- [ ] Sum of predictions vs sum of actuals checked on validation for bias.
