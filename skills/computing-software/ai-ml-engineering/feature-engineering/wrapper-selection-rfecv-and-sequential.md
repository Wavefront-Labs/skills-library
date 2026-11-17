---
id: computing-software.ai-ml-engineering.feature-engineering.wrapper-selection-rfecv-and-sequential
name: wrapper-selection-rfecv-and-sequential
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, feature-selection, rfecv, sequentialfeatureselector, recursive-feature-elimination, wrapper-methods]
level: practitioner
status: verified
description: "Select feature subsets with wrapper methods: RFECV with importance-based elimination and SequentialFeatureSelector forward/backward search, their costs, scoring and nested CV."
sources:
  - https://scikit-learn.org/stable/modules/feature_selection.html#recursive-feature-elimination
  - https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFECV.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SequentialFeatureSelector.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wrapper selection: RFECV and SequentialFeatureSelector

**Goal:** find a smaller feature set that keeps performance, using the model itself to judge subsets.

## RFECV
```python
from sklearn.feature_selection import RFECV
rfe = RFECV(estimator=LogisticRegression(max_iter=2000), step=0.1,          # drop 10% per round
            cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring="roc_auc",
            min_features_to_select=5, n_jobs=-1)
rfe.fit(X_train_scaled, y_train)
rfe.n_features_, rfe.support_, rfe.cv_results_["mean_test_score"]
```
- Checked on 1.9.1: `cv_results_` has `mean_test_score`, `std_test_score`, `n_features` and per-split keys; on 15 features (4 informative) the curve was flat around 0.78-0.79 with 7 chosen at the argmax, and forward SFS with `tol=0.001` picked 5.
- Repeatedly fits, ranks features by `coef_` or `feature_importances_` (or `importance_getter`), and removes the weakest; CV picks the number of features.
- Plot `mean_test_score` vs number of features: usually a plateau - pick the smallest count within noise of the best, not the argmax.
- Linear models need scaled features for coefficient-based ranking; impurity importances from trees favour high-cardinality features.

## SequentialFeatureSelector
```python
from sklearn.feature_selection import SequentialFeatureSelector
sfs = SequentialFeatureSelector(HistGradientBoostingClassifier(), direction="forward",
                                n_features_to_select="auto", tol=0.001, scoring="roc_auc", cv=5, n_jobs=-1)
```
- Greedy: forward adds the feature that most improves CV score; backward removes the least useful. Doesn't need importances, so it works with any model.
- Cost: forward selection of k from p features fits roughly `k x p x cv` models - impractical for hundreds of features with slow models. Pre-filter first.
- `n_features_to_select="auto"` with `tol` stops when gains fall below `tol`.

## Honest evaluation
The selection process overfits the CV folds it searched over. Evaluate the whole procedure (selector + model in a pipeline) with nested CV or on an untouched test set; report that number, not the selector's internal best score.

## When to bother
Wrappers help when features are costly (computation, data purchase, latency) or interpretability needs a short list. For pure accuracy, a well-regularised model on all reasonable features often matches.

## Verify
- [ ] Selection performed inside the evaluation loop (nested CV or test set).
- [ ] Chosen subset size taken from the plateau, with score curve saved.
- [ ] Final subset re-validated on held-out data.
