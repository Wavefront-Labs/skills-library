---
id: computing-software.ai-ml-engineering.scikit-learn.xgboost-and-lightgbm-sklearn-api
name: xgboost-and-lightgbm-sklearn-api
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, xgboost, lightgbm, gradient-boosting, early-stopping, categorical-features]
level: practitioner
status: verified
description: "Use XGBoost and LightGBM through their scikit-learn APIs: key parameters, early stopping with eval_set, native categoricals, and fitting them into Pipelines and CV."
sources:
  - https://xgboost.readthedocs.io/en/stable/python/sklearn_estimator.html
  - https://lightgbm.readthedocs.io/en/latest/Parameters-Tuning.html
  - https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMClassifier.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XGBoost / LightGBM via the sklearn API

`xgboost.XGBClassifier`/`XGBRegressor` and `lightgbm.LGBMClassifier`/`LGBMRegressor` follow the fit/predict API, so they work in `Pipeline`, `GridSearchCV`, `cross_val_score`.

## Starting configs
```python
import xgboost as xgb, lightgbm as lgb
xgbm = xgb.XGBClassifier(n_estimators=5000, learning_rate=0.03, max_depth=6, subsample=0.8,
                         colsample_bytree=0.8, min_child_weight=1, reg_lambda=1.0, tree_method="hist",
                         early_stopping_rounds=100, eval_metric="logloss", n_jobs=-1)
xgbm.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=200)
lgbm = lgb.LGBMClassifier(n_estimators=5000, learning_rate=0.03, num_leaves=63, min_child_samples=20,
                          subsample=0.8, subsample_freq=1, colsample_bytree=0.8, reg_lambda=1.0, n_jobs=-1)
lgbm.fit(X_tr, y_tr, eval_X=X_val, eval_y=y_val, callbacks=[lgb.early_stopping(100), lgb.log_evaluation(200)])   # LightGBM 4.7: eval_set is deprecated (warning), use eval_X/eval_y
print(xgbm.best_iteration, lgbm.best_iteration_)
```
Ran with xgboost 3.4.1 and lightgbm 4.7.0 on 6,000 noisy rows (4,500 train): best iterations 364 (XGBoost) and 253 (LightGBM), validation AUC 0.9545 and 0.9554, against 0.9530 for `HistGradientBoostingClassifier(early_stopping=True)`.
- Lower learning rate + early stopping on a validation set is the standard approach; tune `max_depth`/`num_leaves` and `min_child_*` next, then sampling and regularisation.
- LightGBM grows leaf-wise: control with `num_leaves` (< 2^max_depth); overfits small data if large.
- XGBoost >= 2.0: `early_stopping_rounds` and `eval_metric` are constructor args, not fit args (`fit(..., early_stopping_rounds=5)` raises `TypeError: fit() got an unexpected keyword argument`). `device` is a constructor parameter (it appears in `get_params()`).

## Early stopping inside CV / Pipelines
The validation set must not be the CV test fold (leak). Inside `GridSearchCV`, an estimator built with `early_stopping_rounds` fails without an eval set (`ValueError: Must have at least 1 validation dataset for early stopping.`, reproduced); either fix `n_estimators` from a prior early-stopping run, or carve a validation split from each training fold (custom loop). With a Pipeline, transform the eval set yourself: `eval_set=[(pre.transform(X_val), y_val)]` passed as `model__eval_set` (ran with XGBoost; `model__verbose=False`).

## Categorical features
- LightGBM: pandas `category` dtype is used natively (`categorical_feature="auto"`; ran). Keep train and predict category sets identical (same `CategoricalDtype`); in a test, predicting on a frame whose dtype had an extra category ran without error, so check that the codes map as you expect rather than assuming a failure will flag it.
- XGBoost: `enable_categorical=True` with `tree_method="hist"` and pandas category columns (ran with `max_cat_to_onehot=4`).
- Native categoricals beat one-hot for high cardinality, but can overfit rare levels: `min_data_per_group`, `cat_smooth` (LightGBM), `max_cat_to_onehot` (XGBoost).

## Missing values
Both learn a default direction for NaN at each split; don't impute unless missingness is meaningless.

## Imbalance and probabilities
`scale_pos_weight=neg/pos` (both) or LightGBM `class_weight="balanced"` (ran); XGBoost's sklearn wrapper does not use `class_weight` (it printed `Parameters: { "class_weight" } are not used`; use `scale_pos_weight` or `sample_weight`). Weighting distorts probabilities: calibrate afterwards if needed.

## Gotchas
- `predict` uses the best iteration after early stopping in recent versions (xgboost 3.4.1: default predictions equalled `iteration_range=(0, best_iteration+1)` and differed from all 465 boosted rounds, which include the 100 patience rounds); with older XGBoost pass `iteration_range=(0, best_iteration+1)`.
- `n_jobs=-1` inside an `n_jobs=-1` GridSearchCV oversubscribes CPUs; set one of them to 1.
- Save with the native format (`lgbm.booster_.save_model("m.txt")` / `xgbm.get_booster().save_model("m.json")`; both ran) for version stability.

## Verify
Compare against `HistGradientBoostingClassifier` with early stopping; results should be close. Check `best_iteration` is not at the cap (raise `n_estimators`) or tiny (LR too high).
