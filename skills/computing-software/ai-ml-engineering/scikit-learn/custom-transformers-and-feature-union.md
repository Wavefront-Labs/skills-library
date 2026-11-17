---
id: computing-software.ai-ml-engineering.scikit-learn.custom-transformers-and-feature-union
name: custom-transformers-and-feature-union
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, custom-transformer, basesetimator, transformermixin, columntransformer, featureunion, fit-transform, pipeline, get-feature-names-out, sklearn-api-contract]
level: advanced
status: verified
description: "Write scikit-learn-compatible custom transformers that work inside Pipeline, GridSearchCV and ColumnTransformer, and avoid the fit/transform contract violations that break cloning."
sources:
  - https://scikit-learn.org/stable/developers/develop.html
  - https://scikit-learn.org/stable/modules/compose.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom scikit-learn transformers that actually fit the API contract

**Goal:** write a transformer that composes correctly inside `Pipeline`, `ColumnTransformer`, `GridSearchCV`, and `clone()` — the contract violations here fail silently or only inside cross-validation, not at write-time.

## 1. The contract, and why violating it breaks things you didn't touch
```python
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class LogTransform(TransformerMixin, BaseEstimator):   # mixin FIRST (scikit-learn >= 1.6)
    def __init__(self, cols=None, eps=1e-6):
        self.cols = cols         # store constructor args UNCHANGED, no validation here
        self.eps = eps

    def fit(self, X, y=None):
        self.cols_ = self.cols if self.cols is not None else X.columns.tolist()
        return self              # fit must return self

    def transform(self, X):
        X = X.copy()
        X[self.cols_] = np.log(X[self.cols_] + self.eps)
        return X

    def get_feature_names_out(self, input_features=None):
        return input_features     # needed for ColumnTransformer/Pipeline introspection
```
- **Mixin order: `TransformerMixin` before `BaseEstimator`.** With `(BaseEstimator, TransformerMixin)` on scikit-learn 1.9.1, `check_estimator` stops with "Estimator LogTransform seems to be a Transformer, but the `transformer_tags` tag is not set ... the order of inheritance matter" (tested).
- **`__init__` must store every argument as an attribute with the exact same name, unmodified** — no validation, no derived computation, no renaming. `GridSearchCV`/`clone()` introspects `__init__`'s signature and calls `get_params()`/`set_params()` assuming this exact mapping; doing validation in `__init__` instead of `fit` means `clone()` produces a differently-behaving copy, and this specific bug surfaces only inside `GridSearchCV` (which clones the estimator per fold) — never in a quick standalone test of the transformer.
- **Fitted attributes go in `fit`, named with a trailing underscore** (`self.cols_`, not `self.cols`) — this is the convention scikit-learn tooling (e.g. `check_is_fitted`) relies on to distinguish "configuration the user passed in" from "state learned from data." Mixing these up (storing a fitted value back into the `__init__`-set attribute) breaks `clone()` the same way.
- `fit` returns `self`; `transform` does not take `y` and does not refit — a transformer whose `transform` method depends on anything computed only at `transform`-time rather than remembered from `fit` leaks test-time information and silently gives different results depending on what's in the transform batch (a correctness bug most commonly seen in scalers/encoders someone wrote by hand without this pattern).

## 2. `ColumnTransformer` and `FeatureUnion` specifics
- `ColumnTransformer` lets you apply different transformers to different column subsets and concatenates the outputs — column order in the output is the order the transformers are listed in the constructor, **not** the original DataFrame's column order; code downstream that assumes original column order after a `ColumnTransformer` is a common silent bug. Use `get_feature_names_out()` on the fitted `ColumnTransformer` to get the actual output column names/order rather than guessing.
- `remainder="drop"` (the default) silently drops any column not explicitly assigned to a transformer — if a new column appears in later data versions that wasn't in the original column list, it just vanishes from the model's input with no warning, rather than erroring. Use `remainder="passthrough"` deliberately if you want unlisted columns kept, and add an explicit check elsewhere if new columns should be a loud error, not silent passthrough or silent drop.
- `FeatureUnion` concatenates the outputs of transformers run on the **same** input (unlike `ColumnTransformer`'s column-subset routing) — useful for combining, e.g., a TF-IDF transform and a hand-engineered numeric-feature transform on the same raw text column, but every branch sees the full input, so a branch's `fit` must correctly ignore columns it doesn't need rather than erroring on them.
- Sparse vs dense output mismatches between branches: `FeatureUnion` stacks as sparse as soon as any branch is sparse (tested: TF-IDF plus a dense `FunctionTransformer` column gave a CSR matrix). `ColumnTransformer` is different: when any branch is sparse it stacks sparse only if the overall density is below `sparse_threshold` (default 0.3; `sparse_threshold=0` always returns dense), and an all-dense result is dense (scikit-learn docstring; a tiny TF-IDF plus scaled column came back as a dense `ndarray` in a test). A dense branch next to a wide sparse one can therefore push the combined density over the threshold and materialise a huge dense array; check `ct.sparse_output_` after fitting.

## 3. Debugging checklist when a custom transformer misbehaves only inside `Pipeline`/`GridSearchCV`
- Call `sklearn.utils.estimator_checks.check_estimator(MyTransformer())` (raises on the first failed check by default; `on_fail=None` collects results) — this runs the official conformance test suite and catches most `__init__`/`clone()`/fit-transform contract violations before you ever hit them inside cross-validation. The `LogTransform` above is DataFrame-only (`X.columns`), so 33 of the checks fail on it because they pass NumPy arrays (tested); a transformer meant to pass the suite must accept arrays (use `validate_data` and column indices), otherwise treat the suite as a guide and rely on the manual `clone()` checks below.
- Test `clone(fitted_transformer)` manually and check the clone is unfitted and has the *original* constructor params, not the fitted ones — this is the fastest way to catch the `__init__`-mutation bug directly.
- If `GridSearchCV` results look nonsensical (best params don't actually look best when you refit manually), suspect a transformer that behaves differently when cloned vs when used directly, before suspecting the search itself.

## Verify
- [ ] `check_estimator()` run on the custom transformer and passes (or documented exceptions understood).
- [ ] `__init__` stores every argument unmodified under the same name; no validation/derived state computed there.
- [ ] Fitted-only state lives in trailing-underscore attributes set inside `fit`.
- [ ] `clone()` on a fitted instance produces an unfitted estimator with the original (not fitted) constructor params.
- [ ] `ColumnTransformer`'s `remainder` behavior (drop vs passthrough) is a deliberate choice, and output column order/names are read via `get_feature_names_out()`, not assumed.
- [ ] Sparse/dense mixing across `FeatureUnion`/`ColumnTransformer` branches checked for unexpected densification.
