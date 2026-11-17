---
id: computing-software.ai-ml-engineering.scikit-learn.simple-knn-and-iterative-imputation
name: simple-knn-and-iterative-imputation
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, imputation, simpleimputer, knnimputer, iterativeimputer, missing-indicator, multiple-imputation]
level: practitioner
status: verified
description: "Impute missing values in scikit-learn: SimpleImputer strategies with add_indicator, KNNImputer scaling needs, IterativeImputer (experimental) and when to skip imputation."
sources:
  - https://scikit-learn.org/stable/modules/impute.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.impute.IterativeImputer.html
  - https://scikit-learn.org/stable/auto_examples/impute/plot_missing_values.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SimpleImputer, KNNImputer and IterativeImputer

**Goal:** fill missing values in a way that's leakage-safe, keeps the "was missing" signal, and is as simple as the data allows.

## SimpleImputer + indicator (the strong default)
```python
from sklearn.impute import SimpleImputer
num_imp = SimpleImputer(strategy="median", add_indicator=True)
cat_imp = SimpleImputer(strategy="constant", fill_value="missing")
```
- `add_indicator=True` appends a binary column per feature that had missing values in training (an all-missing training column also got one: 5 features gave 4 imputed + 5 indicator columns, named `missingindicator_x0` and so on). Missingness itself is often predictive (an empty "previous employer" field).
- Median for skewed numerics, mean only for symmetric ones. For categoricals, a constant "missing" category usually beats `most_frequent`.
- `keep_empty_features=True` keeps columns that are entirely missing in a fold (otherwise they are dropped with a `UserWarning: Skipping features without any observed values` and column counts change between folds: output width 4 vs 5 in a test).

## KNNImputer
```python
from sklearn.impute import KNNImputer
pipe = make_pipeline(StandardScaler(), KNNImputer(n_neighbors=5, weights="distance"), model)
```
- Distances use `nan_euclidean`; **scale first**, or large-range features dominate.
- Cost grows with training size (stores the training data, O(n) per query): fitting on 15,000 rows and imputing 5,000 rows x 10 features took 1.1 s here; test your own size before relying on it at 100k+ rows (not measured).

## IterativeImputer (MICE-style)
```python
from sklearn.experimental import enable_iterative_imputer  # noqa: F401  (still required on 1.9.1: importing IterativeImputer without it raises ImportError)
from sklearn.impute import IterativeImputer
imp = IterativeImputer(estimator=BayesianRidge(), max_iter=10, initial_strategy="median",
                       sample_posterior=False, random_state=0)
```
- Models each feature with missing values as a function of the others, round-robin.
- `sample_posterior=True` with different `random_state`s gives multiple imputations (for uncertainty-aware statistical analysis); for prediction pipelines one deterministic imputation is normal.
- Watch `ConvergenceWarning` ("Early stopping criterion not reached", seen with `max_iter=2`); with many features use `n_nearest_features` to bound cost (ran). Without `sample_posterior` two fits with the same `random_state` were identical; with `sample_posterior=True` different seeds gave different imputations.

## When to skip imputation
`HistGradientBoostingClassifier/Regressor`, XGBoost, LightGBM handle NaN natively by learning which branch missing values go to - usually better than imputing. `DecisionTreeClassifier`, `RandomForestClassifier` and `HistGradientBoostingClassifier` all fitted NaN data on 1.9.1 (3-fold CV accuracy on 10% missing synthetic data: 0.887, 0.932 and 0.917).

## Gotchas
- Always fit imputers inside the CV pipeline; imputing on the full dataset leaks test statistics.
- Fancy imputation does not always lose to median + indicator, so benchmark: on the 10%-missing synthetic data with logistic regression, median + indicator scored 0.907, `IterativeImputer` 0.928 and scaled `KNNImputer` 0.927 (3-fold accuracy).
- At serving time, missingness patterns can differ (new form field optional): monitor missing rates per feature.

## Verify
- [ ] Imputer is a pipeline step, fitted per fold.
- [ ] Indicator columns present where missingness is informative.
- [ ] Benchmarked against native-NaN gradient boosting.
