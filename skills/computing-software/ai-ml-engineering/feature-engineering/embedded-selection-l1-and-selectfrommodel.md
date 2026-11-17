---
id: computing-software.ai-ml-engineering.feature-engineering.embedded-selection-l1-and-selectfrommodel
name: embedded-selection-l1-and-selectfrommodel
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, feature-selection, selectfrommodel, l1-selection, lasso, permutation-importance, embedded-methods]
level: practitioner
status: verified
description: "Select features as a side effect of training: L1-regularized linear models, SelectFromModel thresholds, tree importances vs permutation importance, and scaling requirements."
sources:
  - https://scikit-learn.org/stable/modules/feature_selection.html#select-from-model
  - https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectFromModel.html
  - https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embedded selection: L1 and SelectFromModel

**Goal:** let a regularised or tree model decide which features matter, in one training pass.

## L1 (lasso) selection
```python
from sklearn.feature_selection import SelectFromModel
l1 = LogisticRegression(l1_ratio=1, solver="saga", C=0.1, max_iter=5000)   # or LassoCV for regression
# scikit-learn >= 1.8 deprecates penalty="l1" (FutureWarning, removal in 1.10): use l1_ratio=1; before 1.8 use penalty="l1"
pipe = make_pipeline(StandardScaler(), SelectFromModel(l1), HistGradientBoostingClassifier())
```
- L1 drives coefficients exactly to zero; smaller `C` (larger alpha) = fewer features. Tune `C` by CV (`LogisticRegressionCV(l1_ratios=(1.0,), solver="saga")` on 1.8+, `LassoCV`).
- **Scale first** - L1 penalises coefficients, so unscaled features with large ranges are unfairly kept or dropped.
- With correlated features, lasso picks one somewhat arbitrarily; elastic net (`l1_ratio` between 0 and 1) keeps groups more stably.

## SelectFromModel thresholds
- Default threshold: `1e-5` for L1-penalised models, `"mean"` importance otherwise.
- Checked: the threshold resolves to 1e-05 for L1 logistic and `LassoCV`, and to the mean importance (0.05 for 20 features) for a random forest.
- `threshold="median"` keeps half; `"1.25*mean"` stricter; `max_features=30` caps the count.
- `prefit=True` to reuse an already-fitted estimator (careful: then it's outside the CV loop).

## Tree importances: use permutation importance for decisions
Impurity-based `feature_importances_` are biased toward high-cardinality and continuous features and are computed on training data. For selection decisions:
```python
from sklearn.inspection import permutation_importance
r = permutation_importance(model, X_val, y_val, n_repeats=10, random_state=0, scoring="roc_auc")
```
Correlated features share importance (permuting one, the model uses its twin), so both may look unimportant; cluster correlated features and keep one per cluster before permuting.

## Verify
- [ ] Features scaled before L1 selection.
- [ ] Selection step inside the CV pipeline; regularisation tuned by CV.
- [ ] Selection decisions based on validation-set permutation importance, not training impurity importance.
