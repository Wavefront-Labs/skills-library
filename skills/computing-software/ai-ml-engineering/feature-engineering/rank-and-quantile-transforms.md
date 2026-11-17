---
id: computing-software.ai-ml-engineering.feature-engineering.rank-and-quantile-transforms
name: rank-and-quantile-transforms
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, rank-transform, quantile-transform, rank-gauss, percentile-features, outliers, skewed-features]
level: practitioner
status: verified
description: "Turn skewed or outlier-heavy numeric features into ranks, percentiles or Gaussian ranks (RankGauss) with QuantileTransformer, groupwise ranks and leakage-safe fitting."
sources:
  - https://scikit-learn.org/stable/modules/preprocessing.html#quantile-transforms
  - https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.QuantileTransformer.html
  - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rank.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rank and quantile transforms

Replacing a value by its rank discards scale and keeps order. Outliers become just "the largest", heavy tails disappear, and monotone relationships are preserved.

## Who benefits
- Linear models, neural nets, KNN, SVMs: sensitive to scale and outliers.
- Tree models: invariant to monotone transforms of a single feature; ranks change nothing for them (except groupwise or cross-sectional ranks, which are new information).

## Options
```python
from sklearn.preprocessing import QuantileTransformer
qt_u = QuantileTransformer(n_quantiles=1000, output_distribution="uniform", subsample=200_000, random_state=0)  # percentiles in [0,1]
qt_n = QuantileTransformer(n_quantiles=1000, output_distribution="normal", random_state=0)  # "RankGauss": ranks mapped to N(0,1)
```
- Fit on training data inside a Pipeline; transform maps new values through the learned empirical CDF (interpolated between quantiles), so it works on unseen rows and is leakage-safe.
- Values beyond the training range clip to 0/1 (or about +/-5.2 for the normal output): extrapolation is flat (checked). The default `subsample` is 10,000 in current scikit-learn; the 200,000 above is an explicit choice.
- RankGauss (`output_distribution="normal"`) is a common choice for neural-net inputs; benchmark it against log/power transforms.

## pandas rank (in-sample)
```python
df["amt_pct"] = df["amount"].rank(pct=True)               # percentile within the frame
```
This uses the whole frame including validation/test rows when computed before splitting: leakage and train/serve mismatch. Use it only for **cross-sectional features computed per group at prediction time**, e.g.:

## Groupwise / cross-sectional ranks (new information)
```python
df["price_rank_in_category"] = df.groupby("category")["price"].rank(pct=True)
df["return_rank_today"] = df.groupby("date")["ret_1d"].rank(pct=True)      # finance: cross-sectional
```
These are valid when, at prediction time, the whole group is available (all stocks on a date, all listings in a category snapshot). If the group is not fully known when predicting one row, compute the rank against a historical reference distribution instead.

## Ties and discrete features
`rank(method="average")` default; for counts with many zeros, ranks of tied zeros share a value. `QuantileTransformer` on heavily discrete features produces steps; consider log1p instead.

## Choosing between log, power and rank
| Feature | Transform |
|---|---|
| Positive, right-skewed, meaningful ratios | log1p |
| Skewed with negatives | Yeo-Johnson (PowerTransformer) |
| Extreme outliers, unknown shape, NN input | QuantileTransformer (normal) |
| Relative standing within a group | groupwise rank |

## Verify
Compare CV score with and without the transform inside the Pipeline; plot transformed distributions on train vs validation to confirm they match.
