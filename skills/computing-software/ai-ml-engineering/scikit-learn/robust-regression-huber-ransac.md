---
id: computing-software.ai-ml-engineering.scikit-learn.robust-regression-huber-ransac
name: robust-regression-huber-ransac
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, huberregressor, ransac, theilsenregressor, robust-regression, outliers]
level: practitioner
status: verified
description: "Fit regressions that resist outliers: HuberRegressor epsilon, RANSACRegressor residual thresholds and inlier masks, TheilSen, and when to use a robust loss instead."
sources:
  - https://scikit-learn.org/stable/modules/linear_model.html#robustness-regression-outliers-and-modeling-errors
  - https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RANSACRegressor.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Robust regression (Huber, RANSAC, Theil-Sen)

**Problem:** a few corrupted targets (sensor glitches, data-entry errors) drag ordinary least squares far off.

## Which one
| Estimator | Handles | Notes |
|---|---|---|
| `HuberRegressor(epsilon=1.35)` | moderate outliers in y | quadratic loss for small residuals, linear for large; fast; scale-aware |
| `RANSACRegressor` | large fraction of gross outliers in y (and some in X) | fits on random subsets, keeps consensus inliers; non-deterministic |
| `TheilSenRegressor` | outliers in X and y, small dimensions | spatial median of subsample fits; the docs say robustness falls quickly with dimensionality and cost scales combinatorially (cap with `max_subpopulation`); 10,000 x 10 took 2.0 s at the default cap |

## Huber
```python
from sklearn.linear_model import HuberRegressor
hub = make_pipeline(StandardScaler(), HuberRegressor(epsilon=1.35, alpha=1e-4, max_iter=1000)).fit(X, y)
outliers = hub[-1].outliers_          # boolean mask of samples treated as outliers
```
Smaller epsilon is more robust (`epsilon >= 1`); the scikit-learn docs advise 1.35 for 95% statistical efficiency. Test: 200 points with slope 3 (per 1 SD of x) and 20 targets shifted by +40: OLS slope 2.02, Huber 2.81, RANSAC 2.94, Theil-Sen 2.94; Huber flagged 66 points as `outliers_`, more than the 20 planted.

## RANSAC
```python
from sklearn.linear_model import RANSACRegressor, LinearRegression
ransac = RANSACRegressor(LinearRegression(), min_samples=0.5,
                         residual_threshold=None,   # default = MAD of y (docs)
                         max_trials=1000, random_state=0).fit(X, y)
inliers = ransac.inlier_mask_   # 175 of 200 inliers in the test, 20 planted outliers
```
With `LinearRegression` as base, the docs default `min_samples` to `n_features + 1`; the `min_samples=0.5` above is a relative fraction (`ceil(0.5 * n)`).
Set `residual_threshold` in units of y from domain knowledge when MAD is unsuitable. Any estimator can be the base (e.g. polynomial pipeline).

## Alternatives in non-linear models
- `HistGradientBoostingRegressor(loss="absolute_error")` or `"quantile"` (median) for outlier-robust boosting; `GradientBoostingRegressor(loss="huber")` (both fitted without error).
- Robust scaling of features (`RobustScaler`) handles outliers in X but not in y.

## Process
Robust fits are also a diagnostic: inspect samples flagged as outliers. If they are data errors, fix or drop them upstream; if they are real, the model must handle them (and the business may care most about them).

## Verify
- [ ] Compare coefficients and test MAE of OLS vs robust model on data with and without suspected outliers.
