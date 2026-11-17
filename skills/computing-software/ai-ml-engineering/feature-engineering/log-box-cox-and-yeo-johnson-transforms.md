---
id: computing-software.ai-ml-engineering.feature-engineering.log-box-cox-and-yeo-johnson-transforms
name: log-box-cox-and-yeo-johnson-transforms
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, log-transform, box-cox, yeo-johnson, skewed-features, numeric-features]
level: practitioner
status: verified
description: "Transform skewed numeric features with log1p, Box-Cox and Yeo-Johnson, choose by sign and model type, fit inside pipelines, and handle zeros, negatives and back-transforms."
sources:
  - https://scikit-learn.org/stable/modules/preprocessing.html#mapping-to-a-gaussian-distribution
  - https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PowerTransformer.html
  - https://otexts.com/fpp3/transformations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log / Box-Cox / Yeo-Johnson for skewed features

## Why
Income, prices, counts, durations and web traffic are right-skewed with long tails. Linear models, distance-based models and neural nets fit better when such features are closer to symmetric; extreme values stop dominating. **Tree models don't need it** (splits are invariant to monotonic transforms).

## Choose
| Data | Transform |
|---|---|
| Positive, multiplicative effects (prices, income) | `np.log` |
| Non-negative with zeros (counts) | `np.log1p` |
| Strictly positive, want optimal power | Box-Cox (lambda fitted) |
| Any sign, including zero/negative | Yeo-Johnson (lambda fitted) |
| Heavy tails / outliers, want rank-based | `QuantileTransformer(output_distribution="normal")` |
| Signed with large magnitude | `np.sign(x) * np.log1p(np.abs(x))` |

## In a pipeline
```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer, PowerTransformer, StandardScaler
pre = ColumnTransformer([
    ("log", FunctionTransformer(np.log1p, inverse_func=np.expm1, feature_names_out="one-to-one"), ["visits", "orders"]),
    ("yj", PowerTransformer(method="yeo-johnson", standardize=True), ["balance_change"]),
    ("bc", PowerTransformer(method="box-cox"), ["income"]),          # fails on <= 0
    ("num", StandardScaler(), ["age"])])
model = make_pipeline(pre, LogisticRegression(max_iter=2000))
```
`PowerTransformer` fits lambda by maximum likelihood on training folds only (inside CV) and standardises by default. Checked: the pipeline above fits and yields `log__visits`, `yj__balance_change`, `bc__income`, `num__age`; Box-Cox on zero raises exactly that message; a log-normal income column got lambda -0.03. Inspect `pt.lambdas_`: lambda ~ 0 means log-like, 1 means no change, 0.5 square-root-like.

## Target transforms are different
Transforming the target changes what the model predicts: `exp(mean of log y)` is the geometric mean/median, biased low for the mean. Use `TransformedTargetRegressor` and, if the mean is needed, a smearing correction or train with a matching loss (Poisson/Gamma/Tweedie) instead.

## Gotchas
- `np.log(0)` = -inf; `log1p` or a small offset (choose it deliberately; the offset changes the shape near 0).
- Box-Cox on data with zeros raises `ValueError: The Box-Cox transformation can only be applied to strictly positive data`.
- New data outside the training range: transforms still apply but may produce extreme values; clip after transform if needed.
- Interpretability: coefficients on log features are elasticities (percent change), document it.
- Don't transform binary or already-bounded features.

## Verify
Compare skewness (`scipy.stats.skew`) before/after on training data, and CV score of the pipeline with vs without the transform; keep it only if the model improves.
