---
id: computing-software.ai-ml-engineering.scikit-learn.gradient-boosting-tuning-order
name: gradient-boosting-tuning-order
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, boosting-hyperparameters, gradient-boosting, lightgbm, xgboost, histgradientboosting, hyperparameter-tuning]
level: practitioner
status: gated
description: "Tune gradient boosting in the right order: fix learning rate with early stopping, then tree complexity, then sampling and regularization, with ranges for XGBoost/LightGBM/HistGB."
sources:
  - https://lightgbm.readthedocs.io/en/latest/Parameters-Tuning.html
  - https://xgboost.readthedocs.io/en/stable/tutorials/param_tuning.html
  - https://scikit-learn.org/stable/modules/ensemble.html#histogram-based-gradient-boosting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradient boosting tuning order

**Note:** the numeric ranges below are common rules of thumb, not measured here (gated: unconfirmed, source is paywalled or blocked). The parameter names, early stopping and categorical options were run (LightGBM 4.7.0, XGBoost 3.4.1, scikit-learn 1.9.1).

**Principle:** number of trees and learning rate trade off; tree structure controls interaction depth; sampling and penalties control variance. Tune in that order with early stopping so you never tune n_estimators by grid.

## Step 1: learning rate + early stopping
Set `learning_rate=0.05-0.1`, a large `n_estimators` (e.g. 5000) and early stopping on a validation fold (patience 50-200 rounds). Record best iteration.

## Step 2: tree complexity (biggest effect)
| Library | Parameters | Typical ranges |
|---|---|---|
| LightGBM | `num_leaves`, `max_depth`, `min_child_samples` | 15-255, -1 or 4-12, 10-200 |
| XGBoost | `max_depth`, `min_child_weight`, (`max_leaves` with `grow_policy="lossguide"`) | 3-10, 1-20 |
| HistGB (sklearn) | `max_leaf_nodes`, `max_depth`, `min_samples_leaf` | 15-127, None or 3-10, 20-200 |
LightGBM: keep `num_leaves` below 2^max_depth (its Parameters-Tuning page: set `num_leaves` to some value `<= 2^max_depth`; larger can overfit).

## Step 3: sampling
Row subsampling (`subsample`/`bagging_fraction` 0.5-1.0, LightGBM needs `bagging_freq=1`) and column subsampling (`colsample_bytree`/`feature_fraction` 0.5-1.0). HistGB has `max_features` (new in 1.4 per its release notes).

## Step 4: regularization
`reg_lambda`/`lambda_l2` (0-10, log scale), `reg_alpha`/`lambda_l1`, `min_split_gain`/`gamma`. HistGB: `l2_regularization`.

## Step 5: final polish
Lower the learning rate (e.g. 0.01-0.02), re-run early stopping to get more trees: small but reliable gain. Average a few seeds for stability.

## Search tooling
Optuna with pruning over steps 2-4 jointly (TPE sampler, 50-200 trials) works better than grids. Use the same CV folds for all trials.

## Gotchas
- Early stopping on the test set leaks; use a validation split inside the training data (or CV with per-fold early stopping and average best iterations).
- Class imbalance: `scale_pos_weight` (XGBoost/LightGBM) or `class_weight`; evaluate with PR-AUC.
- Categorical handling differs: LightGBM `categorical_feature`, XGBoost `enable_categorical=True` with pandas category dtype, HistGB `categorical_features="from_dtype"`.

## Verify
- [ ] Learning curve of validation metric vs iterations for the final config; best iteration not at the cap.
