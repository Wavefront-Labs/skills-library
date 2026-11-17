---
id: computing-software.ai-ml-engineering.scikit-learn.make-scorer-and-custom-scoring
name: make-scorer-and-custom-scoring
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, make-scorer, scoring, custom-metric, response-method, greater-is-better]
level: practitioner
status: verified
description: "Build custom scikit-learn scorers with make_scorer: greater_is_better, response_method for probabilities, extra kwargs, business-cost scorers and scorer string names."
sources:
  - https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.get_scorer_names.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# make_scorer and custom scoring

A scorer is a callable `scorer(estimator, X, y) -> float` where **higher is better**. Strings like `"roc_auc"`, `"neg_log_loss"`, `"neg_root_mean_squared_error"` map to built-ins (`sklearn.metrics.get_scorer_names()` lists them). Errors are negated (`neg_...`) so that higher is better.

## From a metric function
```python
from sklearn.metrics import make_scorer, fbeta_score, mean_pinball_loss
f2 = make_scorer(fbeta_score, beta=2)                                   # extra kwargs pass through
pinball90 = make_scorer(mean_pinball_loss, alpha=0.9, greater_is_better=False)   # sklearn negates it
```
`greater_is_better=False` makes the scorer return the negated value; grid search results then show negative numbers.

## Probabilities or decision scores
```python
from sklearn.metrics import roc_auc_score, brier_score_loss
auc_ovr = make_scorer(roc_auc_score, response_method="predict_proba", multi_class="ovr")
brier = make_scorer(brier_score_loss, response_method="predict_proba", greater_is_better=False)
```
`response_method` replaces the old `needs_proba`/`needs_threshold` flags, which no longer exist on 1.9.1: `make_scorer(roc_auc_score, needs_proba=True)` builds, then fails when called with `TypeError: ... got an unexpected keyword argument 'needs_proba'` because the kwarg is forwarded to the metric. It accepts a tuple like `("decision_function", "predict_proba")` to use whichever exists. For binary tasks the scorer passes the positive class column.

## Business-cost scorer
```python
def expected_profit(y_true, y_pred, tp_gain=50, fp_cost=5):
    tp = ((y_true == 1) & (y_pred == 1)).sum(); fp = ((y_true == 0) & (y_pred == 1)).sum()
    return tp * tp_gain - fp * fp_cost
profit = make_scorer(expected_profit, tp_gain=50, fp_cost=5)
```
Pair with `TunedThresholdClassifierCV(base, scoring=profit)` to pick the decision threshold that maximises it.

## Full-signature scorer
When the metric needs more than `y_true, y_pred` (e.g. group-aware metrics), write `def scorer(est, X, y): ...` directly and pass it as `scoring=scorer`. Sample weights reach scorers via metadata routing: `make_scorer(...).set_score_request(sample_weight=True)` raises `RuntimeError: This method is only available when metadata routing is enabled` unless you first call `sklearn.set_config(enable_metadata_routing=True)`.

## Multiple metrics
`scoring={"auc": "roc_auc", "f2": f2}` in `cross_validate` or `GridSearchCV(refit="auc")`.

## Gotchas
- Using `"accuracy"` on imbalanced data rewards predicting the majority class.
- `make_scorer(roc_auc_score)` without `response_method` scores hard labels: AUC computed from 0/1 predictions, which is wrong and pessimistic (0.808 vs 0.886 on a synthetic binary problem).
- Label strings: metrics needing `pos_label` (precision, f1 on string labels) take it as a kwarg: `make_scorer(f1_score, pos_label="yes")`; without it string labels fail with `pos_label=1 is not a valid label: It should be one of ['no' 'yes']`.

## Verify
Call the scorer directly on a fitted model and compare with the metric computed by hand on `predict`/`predict_proba` output.
