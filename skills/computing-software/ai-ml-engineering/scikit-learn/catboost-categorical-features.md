---
id: computing-software.ai-ml-engineering.scikit-learn.catboost-categorical-features
name: catboost-categorical-features
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, catboost, categorical-features, ordered-target-statistics, gradient-boosting, cat-features]
level: practitioner
status: gated
description: "Train CatBoost with native categorical handling: cat_features, ordered target statistics, Pool, text features, early stopping, sklearn API integration and pitfalls."
sources:
  - https://catboost.ai/docs/en/concepts/python-quickstart
  - https://catboost.ai/docs/en/features/categorical-features
  - https://catboost.ai/docs/en/references/training-parameters/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CatBoost with categorical features

**Why CatBoost:** strong defaults and built-in categorical encoding with ordered target statistics, which avoids the target leakage of naive target encoding. Good choice for high-cardinality categoricals.

## Basic training
```python
from catboost import CatBoostClassifier, Pool
cat_cols = ["country", "device", "merchant_id"]
train = Pool(X_tr, y_tr, cat_features=cat_cols)
valid = Pool(X_va, y_va, cat_features=cat_cols)
model = CatBoostClassifier(iterations=5000, learning_rate=0.05, depth=6,
                           loss_function="Logloss", eval_metric="AUC",
                           od_type="Iter", od_wait=200, random_seed=0, verbose=200)
model.fit(train, eval_set=valid, use_best_model=True)
```
- Categorical columns must be strings or ints. A float value or NaN in a `cat_features` column makes `Pool(...)` raise `Invalid type for cat_feature ... cat_features must be integer or string` (tested, catboost 1.2.10); fill NaN categoricals with a sentinel like `"__missing__"` and cast to str.
- No one-hot or target encoding beforehand; pass raw categories.
- `one_hot_max_size` (default small) one-hot encodes low-cardinality features; above it, CTR statistics are used.
- Feature combinations of categoricals are generated automatically (controlled by `max_ctr_complexity`).

## Text and embeddings
`text_features=[...]` for raw text columns (built-in tokenization and BoW/NB estimators); `embedding_features=` for vector columns.

## In sklearn pipelines
CatBoost estimators follow the sklearn API (`fit/predict/predict_proba`, `get_params`). `cat_features` given in the constructor made `sklearn.base.clone` fail (`Cannot clone object ... modifies parameter cat_features`, tested on catboost 1.2.10 with scikit-learn 1.9.1), which breaks `cross_val_score`/`GridSearchCV`. Pass it at fit time instead: `GridSearchCV(...).fit(X, y, cat_features=cols)`, `Pipeline.fit(X, y, m__cat_features=cols)` and `cross_val_score(m, X, y, params={"cat_features": cols})` all worked (tested). Keep columns as a DataFrame (no ColumnTransformer that converts to numpy without names).

## Tuning
Main knobs: `learning_rate`, `depth` (4-10), `l2_leaf_reg`, `iterations` with early stopping, `bagging_temperature` / `subsample`. Use `grow_policy="Lossguide"` for LightGBM-like leaf-wise trees. GPU: `task_type="GPU"` (gated: unconfirmed, source is paywalled or blocked).

## Pitfalls
- Keep category values identical between training and serving. Integer categories predicted as `int` after training on `str` gave identical probabilities (tested), so int-versus-str alone did not change predictions; do not assume a type mismatch makes categories "new".
- `use_best_model=True` without an eval set is switched off with the message "You should provide test set for use best model" (tested), so you keep all iterations (overfit).
- Feature importance: prefer `get_feature_importance(type="PredictionValuesChange")` or SHAP (`type="ShapValues"`).

## Verify
- [ ] Compare against HistGradientBoosting with OrdinalEncoder on the same CV folds.
- [ ] Save with `model.save_model("m.cbm")` and reload; predictions match.
