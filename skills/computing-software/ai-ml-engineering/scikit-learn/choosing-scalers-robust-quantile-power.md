---
id: computing-software.ai-ml-engineering.scikit-learn.choosing-scalers-robust-quantile-power
name: choosing-scalers-robust-quantile-power
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, sklearn-preprocessing, feature-scaling, standardscaler, robustscaler, quantiletransformer, powertransformer, maxabsscaler, scaling-choice, min-max-scaling]
level: practitioner
status: verified
description: "Pick the right scikit-learn scaler: Standard, MinMax, MaxAbs for sparse, Robust for outliers, QuantileTransformer and PowerTransformer for skew, and which models need none."
sources:
  - https://scikit-learn.org/stable/modules/preprocessing.html
  - https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PowerTransformer.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Choosing scalers: Standard, Robust, Quantile, Power

**Goal:** scale numeric features in a way that helps the model you're using and survives outliers and skew.

## Who needs scaling
- **Needs it:** linear/logistic regression with regularisation (penalty treats coefficients equally), SVMs, KNN, K-means, PCA, neural nets, anything with distances or gradient descent.
- **Doesn't:** tree-based models (decision trees, random forests, gradient boosting) - splits are invariant to monotonic transforms.

## The options
| Scaler | What it does | Use when |
|---|---|---|
| `StandardScaler` | subtract mean, divide by std | default for roughly symmetric features |
| `MinMaxScaler` | map to [0, 1] | bounded features, NN inputs needing a fixed range; outliers squash everything else |
| `MaxAbsScaler` | divide by max abs | **sparse** data (keeps zeros zero) |
| `RobustScaler` | subtract median, divide by IQR (`quantile_range=(25, 75)`) | outliers present; outliers remain large but don't distort the rest |
| `PowerTransformer` | Yeo-Johnson (default) or Box-Cox (positive only), then standardise | skewed features for linear models; makes data more Gaussian |
| `QuantileTransformer` | map to uniform or normal via empirical CDF | heavy tails, outliers; non-linear, strongest normalisation |
| `Normalizer` | scales each **row** to unit norm | text/TF-IDF vectors, cosine similarity - not a column scaler |

## Examples
```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler, PowerTransformer, QuantileTransformer
pre = ColumnTransformer([
    ("skewed", PowerTransformer(method="yeo-johnson"), ["income", "balance"]),
    ("outliers", RobustScaler(), ["age", "tenure"]),
    ("heavy", QuantileTransformer(output_distribution="normal", n_quantiles=1000, random_state=0), ["txn_amount"]),
])
```

## Gotchas
- Fit scalers inside the `Pipeline` so CV folds fit them on training data only.
- `QuantileTransformer` with `n_quantiles` > n_samples warns; it's also non-linear, so it distorts linear relationships and makes extrapolation flat (values beyond the training range clip to the extremes).
- `StandardScaler(with_mean=False)` is required for sparse matrices (centering densifies them).
- Box-Cox fails on zeros/negatives; Yeo-Johnson handles them.
- Scaling changes regularisation strength meaning: retune `C`/`alpha` after changing scaler.

## Verify
- [ ] Scaler chosen per feature group based on distribution plots, not one-size-fits-all.
- [ ] Scaler fitted inside the pipeline.
- [ ] CV score compared across scaler choices for the linear/distance model.
