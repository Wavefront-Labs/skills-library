---
id: computing-software.ai-ml-engineering.model-training.holdout-vs-kfold-vs-bootstrap-validation
name: holdout-vs-kfold-vs-bootstrap-validation
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, bootstrap-validation, k-fold, holdout, out-of-bag, validation-strategy, optimism-bootstrap]
level: practitioner
status: draft
description: "Choose between holdout, k-fold, repeated CV and bootstrap validation by data size, model cost and need for uncertainty, including .632 bootstrap and optimism correction."
sources:
  - https://scikit-learn.org/stable/modules/cross_validation.html
  - https://hastie.su.domains/ElemStatLearn/
  - https://scikit-learn.org/stable/modules/generated/sklearn.utils.resample.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Holdout vs k-fold vs bootstrap

## Decision guide
| Situation | Use |
|---|---|
| Large data (100k+ rows), expensive models (deep learning) | single holdout (train/val/test) |
| Small/medium tabular data, cheap models | k-fold (5 or 10), stratified for classification |
| Very small data (< few hundred), need stable estimates | repeated k-fold (e.g. 5x10) or bootstrap |
| Need confidence intervals for a metric | bootstrap the test predictions, or repeated CV |
| Hyperparameter tuning + unbiased estimate | nested CV, or CV for tuning + untouched test set |
| Groups / time | GroupKFold / TimeSeriesSplit regardless of the above |

## Holdout
Cheap and simple; variance of the estimate is high for small test sets (a 500-row test set gives about +/- 4 points on accuracy at 95%). Fine when test sets have thousands of examples.

## k-fold
Uses all data for both training and evaluation; standard error across folds underestimates true uncertainty (folds share training data) but is useful for comparing models. Larger k: less bias (training sets closer to full size), more compute and more variance per fold. k=5 or 10 is the usual compromise.

## Bootstrap validation
Train on a bootstrap sample (n rows drawn with replacement), evaluate on out-of-bag rows (~36.8% left out), repeat B = 100-500 times.
```python
from sklearn.utils import resample
scores = []
for b in range(200):
    idx = resample(np.arange(n), replace=True, random_state=b)
    oob = np.setdiff1d(np.arange(n), idx)
    m = clone(model).fit(X[idx], y[idx]); scores.append(metric(y[oob], m.predict(X[oob])))
```
- OOB estimate is pessimistic (each model sees only ~63.2% unique rows). The **.632 estimator** blends it with the optimistic training error: `0.368 * err_train + 0.632 * err_oob`; .632+ corrects further for overfitting models.
- **Optimism bootstrap** (Harrell; common in clinical prediction models): fit on bootstrap sample, measure performance on bootstrap sample minus on original data = optimism; average and subtract from apparent performance.
- Random forests give OOB estimates for free (`oob_score=True`).

## Bootstrap for confidence intervals (separate use)
Fixed model, fixed test set: resample test rows to get the sampling distribution of the metric. This measures test-set noise, not training variability.

## Gotchas
- Preprocessing and feature selection must happen inside each resample/fold (Pipeline), or all methods are optimistic.
- Duplicates in bootstrap samples can inflate performance for models that memorise (KNN, 1-NN): use OOB, not in-bag.
