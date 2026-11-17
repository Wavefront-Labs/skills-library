---
id: computing-software.ai-ml-engineering.scikit-learn.custom-estimator-passing-check-estimator
name: custom-estimator-passing-check-estimator
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, custom-estimator, check-estimator, parametrize-with-checks, sklearn-api-contract, validate-data, baseestimator]
level: practitioner
status: verified
description: "Write a scikit-learn compatible estimator: __init__ rules, fit returning self, trailing-underscore attributes, validate_data, check_is_fitted, and testing with check_estimator."
sources:
  - https://scikit-learn.org/stable/developers/develop.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.utils.estimator_checks.check_estimator.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.utils.estimator_checks.parametrize_with_checks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# A custom estimator that passes check_estimator

**Goal:** an estimator that works with `Pipeline`, `GridSearchCV`, `clone` and cross-validation, proven by the official test suite.

## Template
```python
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_is_fitted, validate_data   # validate_data: sklearn >= 1.6
from sklearn.utils.multiclass import unique_labels

class NearestCentroidLite(ClassifierMixin, BaseEstimator):      # mixins BEFORE BaseEstimator
    def __init__(self, metric="euclidean", shrink=0.0):
        self.metric = metric          # store params verbatim: no validation, no logic, no defaults derived here
        self.shrink = shrink

    def fit(self, X, y):
        X, y = validate_data(self, X, y)          # sets n_features_in_ (and feature_names_in_ for DataFrames)
        if self.shrink < 0:
            raise ValueError("shrink must be >= 0")   # validate params in fit, not __init__
        self.classes_ = unique_labels(y)
        self.centroids_ = np.vstack([X[y == c].mean(axis=0) for c in self.classes_])
        return self                               # always return self

    def predict(self, X):
        check_is_fitted(self)
        X = validate_data(self, X, reset=False)   # checks n_features matches fit
        d = ((X[:, None, :] - self.centroids_[None]) ** 2).sum(-1)
        return self.classes_[d.argmin(axis=1)]
```
On scikit-learn < 1.6, use `self._validate_data(X, y)` instead of `validate_data(self, X, y)`.

## The contract
- `__init__` arguments are keyword, stored under the same names, and not modified - `get_params`/`set_params`/`clone` depend on it.
- Attributes learned in `fit` end with `_` (`coef_`, `classes_`); none are created in `__init__`.
- `fit` returns `self`; `fit` called twice must forget the first fit.
- Randomness through `random_state` + `check_random_state(self.random_state)` inside `fit`.
- Classifiers set `classes_`; transformers implement `fit`/`transform` (via `TransformerMixin` get `fit_transform`) and ideally `get_feature_names_out`.

## Test it
```python
from sklearn.utils.estimator_checks import parametrize_with_checks
@parametrize_with_checks([NearestCentroidLite()])
def test_sklearn_compatible(estimator, check):
    check(estimator)
```
Run with pytest; each check is a separate test, so failures are readable. `check_estimator(NearestCentroidLite())` runs them all in one call. Some checks may not apply (e.g. your estimator requires positive inputs); declare that via estimator tags (`__sklearn_tags__` in >= 1.6) rather than skipping checks blindly.

## Verify
- [ ] `parametrize_with_checks` suite passes.
- [ ] `clone(est)` and `GridSearchCV(est, {...})` work.
- [ ] Works as a step inside a `Pipeline` with a `ColumnTransformer` in front.
