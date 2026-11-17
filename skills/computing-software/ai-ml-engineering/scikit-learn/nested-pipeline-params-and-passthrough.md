---
id: computing-software.ai-ml-engineering.scikit-learn.nested-pipeline-params-and-passthrough
name: nested-pipeline-params-and-passthrough
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, nested-params, pipeline, gridsearchcv, passthrough, set-params, step-replacement]
level: practitioner
status: verified
description: "Tune nested pipeline parameters with step__param syntax, swap whole steps or set them to passthrough/drop in a grid, and inspect get_params safely."
sources:
  - https://scikit-learn.org/stable/modules/compose.html#nested-parameters
  - https://scikit-learn.org/stable/modules/grid_search.html#composite-estimators-and-parameter-spaces
  - https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Nested pipeline parameters and passthrough steps

**Goal:** search over preprocessing choices and model hyperparameters in one cross-validated search, without leakage.

## Syntax
`<step>__<param>`, chaining through levels: `columntransformer__num__simpleimputer__strategy`.
```python
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

pipe = Pipeline([("scale", StandardScaler()), ("reduce", PCA()), ("clf", LogisticRegression(max_iter=2000))])
param_grid = [
    {"reduce": [PCA()], "reduce__n_components": [10, 30, 50],
     "clf": [LogisticRegression(max_iter=2000)], "clf__C": [0.1, 1, 10]},
    {"reduce": [SelectKBest()], "reduce__k": [10, 30],
     "clf": [SVC()], "clf__C": [1, 10], "clf__gamma": ["scale", 0.01]},
    {"reduce": ["passthrough"], "clf": [LogisticRegression(max_iter=2000)], "clf__C": [1]},
]
search = GridSearchCV(pipe, param_grid, cv=5, scoring="roc_auc", n_jobs=-1).fit(X, y)
```
- A list of dicts defines separate sub-grids, so parameters only apply to the estimator that has them.
- `"passthrough"` (or `None`) skips a Pipeline step; in a ColumnTransformer use `"drop"` or `"passthrough"` for a transformer.
- Replacing a step with an estimator instance is a valid grid value.

## Discover names
```python
sorted(pipe.get_params().keys())        # every settable path
```
Typos raise `ValueError: Invalid parameter 'Cc' for estimator LogisticRegression(max_iter=2000). Valid parameters are: [...]` from both `set_params` and `GridSearchCV.fit`, which is helpful; the grid above (18 candidates) ran on 1.9.1, with `None` and `"passthrough"` both accepted as the `reduce` value; misnamed steps from `make_pipeline` auto-names are the usual cause.

## set_params outside search
`pipe.set_params(clf__C=3, reduce="passthrough")` mutates in place; clone first if the pipeline is shared (`sklearn.base.clone`).

## Reading results
`search.cv_results_["params"]` contains estimator objects; convert to strings for logging (`{k: str(v) for k, v in p.items()}`). `search.best_estimator_` is refit on all data with the winning step choices.

## Verify
- [ ] Grid size (`len(ParameterGrid(param_grid))`) times folds is affordable before running.
- [ ] Best params printed and best pipeline's steps are the expected classes.
