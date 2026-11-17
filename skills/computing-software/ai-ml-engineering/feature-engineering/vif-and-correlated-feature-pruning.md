---
id: computing-software.ai-ml-engineering.feature-engineering.vif-and-correlated-feature-pruning
name: vif-and-correlated-feature-pruning
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, vif, multicollinearity, variance-inflation-factor, correlation-pruning, feature-selection, statsmodels]
level: practitioner
status: verified
description: "Detect multicollinearity with variance inflation factors and correlation clustering, prune redundant features for linear models, and know when collinearity does not matter."
sources:
  - https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html
  - https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance_multicollinear.html
  - https://en.wikipedia.org/wiki/Variance_inflation_factor
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multicollinearity (VIF) and correlated-feature pruning

## When it matters
- **Inference / interpretation** with linear or logistic regression: collinearity inflates coefficient variance, flips signs and makes p-values meaningless.
- **Unregularised linear models**: unstable fits.
- **Not much** for prediction with regularised models (ridge handles it) or trees (they pick one of the correlated features; importance splits).

## VIF
VIF_j = 1 / (1 - R_j^2), where R_j^2 comes from regressing feature j on all others. VIF 1 = no collinearity; > 5 notable; > 10 severe (common rules of thumb).
```python
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
Xc = add_constant(X_num.dropna())              # intercept: needed on older statsmodels (no-intercept VIFs are uncentred and inflated)
# statsmodels 0.15 standardises columns by default (standardize=True), so the constant no longer changes the result (checked: identical VIFs); pass standardize=False for the old behaviour
vif = pd.Series([variance_inflation_factor(Xc.values, i) for i in range(Xc.shape[1])], index=Xc.columns).drop("const")
vif.sort_values(ascending=False)
```
- One-hot dummies: drop one level per categorical (or VIF is infinite). Generalised VIF (GVIF) handles multi-column categoricals.
- Iterative pruning: remove the highest-VIF feature, recompute, repeat until all below threshold. Prefer removing the less interpretable or less reliable feature of a group rather than strictly the highest VIF.

## Correlation-based pruning
```python
corr = X_num.corr(method="spearman").abs()
upper = corr.where(np.triu(np.ones(corr.shape, dtype=bool), k=1))
to_drop = [c for c in upper.columns if (upper[c] > 0.95).any()]
```
Pairwise correlation misses multi-feature collinearity (a = b + c) that VIF catches. Hierarchical clustering on `1 - |spearman|` gives groups to keep one representative from.

## Alternatives to dropping
- Combine correlated features (sum, average, ratio, PCA within the group) into one interpretable index.
- Ridge / elastic net for prediction.
- Centre variables before creating interaction or polynomial terms (reduces structural collinearity).

## Inside pipelines
VIF/correlation pruning uses only X (no target), so it does not leak labels, but still fit on training data only for consistency. A small custom transformer computing the drop list in `fit` keeps it reproducible.

## Verify
After pruning: coefficients stable across bootstrap resamples, VIFs below threshold, and CV score unchanged (if it drops, you removed information, not redundancy).
