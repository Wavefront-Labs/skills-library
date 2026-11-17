---
id: computing-software.ai-ml-engineering.scikit-learn.dummy-baselines
name: dummy-baselines
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, dummyclassifier, dummyregressor, baselines, model-evaluation, sanity-check]
level: practitioner
status: verified
description: "Establish trivial baselines with DummyClassifier/DummyRegressor strategies (most_frequent, prior, stratified, mean, median, quantile) and compare every model against them."
sources:
  - https://scikit-learn.org/stable/modules/model_evaluation.html#dummy-estimators
  - https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dummy baselines

**Why:** a 95% accuracy model is worthless when 95% of samples are one class. Always report the trivial baseline alongside your model, on the same folds and metric.

## Classifier strategies
| strategy | Predicts | Useful for |
|---|---|---|
| `most_frequent` | majority class; proba one-hot | accuracy baseline |
| `prior` | majority class; proba = class priors | log-loss / Brier baseline |
| `stratified` | random draws from priors | random-guess F1/precision baseline |
| `uniform` | uniform random class | multiclass chance |
| `constant` (`constant=1`) | always that label | recall=1 baseline for the positive class |

## Regressor strategies
`mean` (R^2 = 0 on the data it was fitted on; in cross-validation it is slightly negative, -0.34 in a 100-sample test, because each fold's mean differs from the test fold), `median` (MAE baseline), `quantile` (`quantile=0.9`, pinball baseline), `constant`.

## Usage
```python
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import cross_validate
for name, est in {"dummy": DummyClassifier(strategy="prior"), "model": pipe}.items():
    r = cross_validate(est, X, y, cv=cv, scoring=["roc_auc", "average_precision", "neg_log_loss"])
    print(name, {k: v.mean().round(4) for k, v in r.items() if k.startswith("test_")})
```
Expected dummy values (computed with `prior` on 10% positives, 5-fold stratified): ROC-AUC 0.5, average precision 0.0965 = the positive rate, log loss 0.3173 = entropy of the prior. `most_frequent` and `stratified` return one-hot `predict_proba`, `prior` returns the class priors, `uniform` 0.5/0.5 (tested).

## Stronger baselines
After the dummy, add a simple domain baseline: last value / seasonal naive for forecasting, logistic regression on a few obvious features, or the current business rule. A new model should beat the best simple baseline, not just the dummy.

## Verify
- [ ] Every evaluation report includes dummy and simple-baseline rows.
