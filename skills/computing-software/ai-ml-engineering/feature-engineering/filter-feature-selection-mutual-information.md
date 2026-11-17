---
id: computing-software.ai-ml-engineering.feature-engineering.filter-feature-selection-mutual-information
name: filter-feature-selection-mutual-information
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, feature-selection, mutual-information, variancethreshold, selectkbest, correlation-pruning, univariate-selection]
level: practitioner
status: verified
description: "Cut features cheaply with filter methods: VarianceThreshold, correlation pruning, SelectKBest with mutual information or F-tests, their blind spots and leakage-safe use."
sources:
  - https://scikit-learn.org/stable/modules/feature_selection.html#univariate-feature-selection
  - https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_classif.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.VarianceThreshold.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filter feature selection: variance, correlation, mutual information

**Goal:** remove useless and redundant features fast, before or instead of expensive selection methods.

## Remove constants and near-constants
```python
from sklearn.feature_selection import VarianceThreshold
vt = VarianceThreshold(threshold=0.0)        # drops constant columns; for binary features p(1-p) < 0.01 is ~99% one value
```
Variance depends on scale: use it on unscaled binary/count data or after deciding a per-feature threshold.

## Prune redundant features
```python
corr = X_train.corr(method="spearman").abs()
upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
drop = [c for c in upper.columns if (upper[c] > 0.95).any()]
```
Keep the more interpretable or cheaper-to-compute member of each correlated pair. Highly correlated features make coefficient and importance interpretation unstable even when predictions are fine.

## Univariate relevance
```python
from sklearn.feature_selection import SelectKBest, mutual_info_classif, f_classif, chi2
from functools import partial
mi = partial(mutual_info_classif, discrete_features=disc_mask, random_state=0)
sel = SelectKBest(score_func=mi, k=50)          # or SelectPercentile
```
- **Mutual information:** captures non-linear dependence; kNN-based estimate is noisy on small data - set `random_state`, and mark discrete features correctly.
- **f_classif / f_regression:** linear dependence only; fast.
- **chi2:** for non-negative features (counts, TF-IDF).

## Blind spots
Checked: the Spearman upper-triangle prune flagged a feature built as 2*a + small noise, and `SelectKBest` with a `partial(mutual_info_classif, discrete_features=mask, random_state=0)` score function ran and selected the informative columns.

Univariate filters ignore interactions (a feature useless alone but powerful with another) and redundancy (they'll pick 10 copies of the same signal). Use them to cut obvious noise from very wide data (thousands of features), then rely on regularised models or model-based selection.

## Leakage
Any filter that uses `y` must be inside the CV pipeline; otherwise it selects on validation labels and inflates scores (classic selection bias on wide data).

## Verify
- [ ] Filters with labels sit inside the pipeline.
- [ ] CV score with selection >= without (or simpler model at equal score).
- [ ] Dropped-feature list saved with the model.
