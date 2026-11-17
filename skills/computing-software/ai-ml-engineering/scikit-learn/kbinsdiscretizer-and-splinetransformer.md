---
id: computing-software.ai-ml-engineering.scikit-learn.kbinsdiscretizer-and-splinetransformer
name: kbinsdiscretizer-and-splinetransformer
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, sklearn-preprocessing, kbinsdiscretizer, splinetransformer, binning, periodic-splines, nonlinear-features]
level: practitioner
status: verified
description: "Give linear models non-linear power with KBinsDiscretizer (quantile, uniform, kmeans) and SplineTransformer, including periodic splines for hours, days and seasons."
sources:
  - https://scikit-learn.org/stable/modules/preprocessing.html#discretization
  - https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.SplineTransformer.html
  - https://scikit-learn.org/stable/auto_examples/applications/plot_cyclical_feature_engineering.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KBinsDiscretizer and SplineTransformer

**Goal:** model non-linear effects of a numeric feature inside an interpretable linear model.

## KBinsDiscretizer
```python
from sklearn.preprocessing import KBinsDiscretizer
kb = KBinsDiscretizer(n_bins=10, encode="onehot", strategy="quantile")   # also "uniform", "kmeans"
```
- `quantile`: equal counts per bin - robust to skew and outliers (default choice).
- `uniform`: equal widths - outliers create empty bins (lognormal data, 10 bins: counts 428, 56, 10, 1, 2, 2, 0, 0, 0, 1; `quantile` gave 50 each; tested).
- `kmeans`: bins around 1-D cluster centres.
- `encode="onehot"` gives a piecewise-constant effect in a linear model; `"ordinal"` gives one integer column (useful for trees or further encoding).
- Too many bins with few samples per bin overfits; combine with regularisation.
- Gives step functions - prediction jumps at bin edges.

## SplineTransformer (smooth)
```python
from sklearn.preprocessing import SplineTransformer
spl = SplineTransformer(n_knots=6, degree=3, knots="quantile", extrapolation="constant")
model = make_pipeline(ColumnTransformer([("spl", spl, ["age"])], remainder="passthrough"), RidgeCV())
```
- B-spline basis features; a linear model on top fits a smooth curve. `n_bins = n_knots - 1`; number of output features is `n_knots + degree - 1` per input (8 for 6 knots and degree 3, tested).
- `knots="quantile"` puts knots where data is dense.
- `extrapolation="constant"`/`"linear"` controls behaviour outside the training range (default `"constant"`); be deliberate - polynomial-like extrapolation is dangerous.

## Periodic features (hour, day-of-week, month)
```python
hour_spline = SplineTransformer(n_knots=13, degree=3, knots=np.linspace(0, 24, 13).reshape(-1, 1),
                                extrapolation="periodic")
```
`extrapolation="periodic"` makes hour 0 and hour 24 map to identical features and 23:00 close to 00:00 (tested) - better than one-hot (no smoothness) or raw hour (no wrap-around) and more flexible than a single sin/cos pair.

## Interactions
Splines on two features followed by `PolynomialFeatures(degree=2, interaction_only=True)` or a kernel approximation (`Nystroem`) capture interactions such as "hour x weekday".

## Verify
- [ ] Partial-dependence plot of the fitted model shows a plausible shape (no wild wiggles at the edges).
- [ ] CV score compared with the raw-feature linear model and with a GBM baseline.
- [ ] Out-of-range behaviour checked with values beyond the training min/max.
