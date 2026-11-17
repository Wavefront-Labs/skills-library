---
id: computing-software.ai-ml-engineering.scikit-learn.cross-validate-and-cross-val-predict
name: cross-validate-and-cross-val-predict
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, cross-val-predict, cross-validate, return-train-score, out-of-fold-predictions, cross-validation]
level: practitioner
status: verified
description: "Use cross_validate for multi-metric scores, fit/score times, train scores and fitted estimators, and cross_val_predict for out-of-fold predictions without misusing them."
sources:
  - https://scikit-learn.org/stable/modules/cross_validation.html#the-cross-validate-function-and-multiple-metric-evaluation
  - https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_predict.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# cross_validate and cross_val_predict

## cross_validate
```python
from sklearn.model_selection import cross_validate, StratifiedKFold
cv = StratifiedKFold(5, shuffle=True, random_state=0)
res = cross_validate(pipe, X, y, cv=cv,
                     scoring={"auc": "roc_auc", "ap": "average_precision", "logloss": "neg_log_loss"},
                     return_train_score=True, return_estimator=True,
                     return_indices=True, n_jobs=-1, error_score="raise")
import pandas as pd
print(pd.DataFrame({k: v for k, v in res.items() if k.startswith("test_")}).agg(["mean", "std"]))
```
- Returns `fit_time`, `score_time`, `test_<metric>`, and with flags `train_<metric>`, `estimator`, `indices`.
- Train vs test gap per fold diagnoses overfitting; std across folds tells you whether differences between models are meaningful.
- `error_score="raise"` surfaces fit failures instead of silently scoring NaN.
- `pd.DataFrame(res)` on the whole result raises `ValueError: Mixing dicts with non-Series` when `return_indices=True` (the `indices` entry is a dict), so select the `test_`/`train_` keys first (tested, scikit-learn 1.9.1).
- `params={"sample_weight": w}` passes fit params per fold. With metadata routing off it went to `fit` and worked; with `set_config(enable_metadata_routing=True)` it raised until the request was set on the estimator and the scorer (`set_fit_request` / `set_score_request`).

## cross_val_predict
Returns an out-of-fold prediction for every sample (each predicted by the model that did not see it).
```python
from sklearn.model_selection import cross_val_predict
oof_proba = cross_val_predict(pipe, X, y, cv=cv, method="predict_proba", n_jobs=-1)[:, 1]
```
Legitimate uses: confusion matrices and error analysis on all data, stacking features (meta-learner inputs), calibration analysis, label-noise detection.

## Do not
- Report a single metric computed on `cross_val_predict` output as the CV score: it pools folds trained on different models and can differ from the mean of fold scores (notably for AUC and ranking metrics; tested: pooled AUC 0.886 vs mean fold AUC 0.891). Use `cross_validate` for the estimate.
- Use either for hyperparameter selection and then report the same number as final performance; that needs nested CV or a held-out test set.

## Splitters
Requires a partition (every sample in exactly one test fold) for `cross_val_predict`; `TimeSeriesSplit` and `ShuffleSplit` are not partitions and raise an error.

## Verify
- [ ] Fold scores table logged with mean and std; train/test gap inspected.
