---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.train-test-cross-validation
name: train-test-cross-validation
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [train-test-split, cross-validation, overfitting-check]
level: practitioner
status: docs-checked
description: "Estimate generalisation error with held-out splits and k-fold cross-validation, keeping preprocessing inside the folds to avoid leakage."
sources:
  - https://scikit-learn.org/stable/modules/cross_validation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Out-of-sample validation (scikit-learn)
```python
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
```
## Gotchas
- `cross_val_score` is the simplest helper for cross-validation.
- Knowledge about the test set can "leak" into the model if you tune on it; hold out data for the final check.
- A `Pipeline` composes estimators so preprocessing is refit inside each cross-validation fold; build preprocessing into the pipeline (the guide uses `make_pipeline`).
- Time series: `TimeSeriesSplit` trains on the first k folds and tests on the next, instead of shuffled folds.
- Grouped rows (same customer): `GroupKFold` keeps a group out of both train and test sets.

## Verify
- [ ] Train error much lower than CV error signals overfit.

## Checked

2026-11-02. Confirmed against the scikit-learn cross-validation page (cross_val_score, leakage note, Pipeline, TimeSeriesSplit, GroupKFold). Removed: Ridge/StandardScaler/KFold arguments and the neg_root_mean_squared_error scoring name (not found on the page read).
Method: documentation only; no commands were run.
