---
id: computing-software.ai-ml-engineering.scikit-learn.multimetric-scoring-and-refit
name: multimetric-scoring-and-refit
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, multimetric-scoring, refit-strategy, gridsearchcv, cross-validate, one-standard-error-rule, scoring]
level: practitioner
status: verified
description: "Evaluate several metrics in one CV search and choose the final model with refit: metric names, callable refit (one-standard-error rule), and cv_results_ keys."
sources:
  - https://scikit-learn.org/stable/modules/grid_search.html#multimetric-grid-search
  - https://scikit-learn.org/stable/auto_examples/model_selection/plot_grid_search_refit_callable.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-metric scoring and refit

**Goal:** see the trade-offs between metrics during model selection and refit the model on the metric that actually matters.

## Multiple metrics
```python
scoring = {"auc": "roc_auc", "ap": "average_precision",
           "recall": make_scorer(recall_score), "f1": "f1"}
search = GridSearchCV(pipe, grid, cv=cv, scoring=scoring, refit="ap", n_jobs=-1, return_train_score=True)
search.fit(X, y)
pd.DataFrame(search.cv_results_)[["params", "mean_test_auc", "mean_test_ap", "std_test_ap", "rank_test_ap"]]
```
- `cv_results_` gets `mean_test_<name>`, `std_test_<name>`, `rank_test_<name>` per metric.
- With several metrics `refit` must name one (or be a callable, or `False`). `best_params_`, `best_score_` and `best_estimator_` refer to that metric.
- `cross_validate(est, X, y, scoring=scoring)` does the same for a single model, returning `test_<name>` arrays.
- Each scorer is computed on the same fitted fold model, so adding metrics costs prediction time only.

## Callable refit: prefer simpler models
Pick the simplest model within one standard error of the best (Breiman's 1-SE rule):
```python
def one_se(cv_results):
    mean, std = cv_results["mean_test_ap"], cv_results["std_test_ap"]
    best = np.argmax(mean)
    thresh = mean[best] - std[best]
    ok = np.flatnonzero(mean >= thresh)
    # simplest = smallest C (stronger regularisation)
    cs = np.array(cv_results["param_clf__C"], dtype=float)
    return ok[np.argmin(cs[ok])]
search = GridSearchCV(pipe, grid, cv=cv, scoring=scoring, refit=one_se)
```
- The callable receives `cv_results_` and returns an index. With a callable refit, `best_score_` is not set (`best_index_`, `best_params_` and `best_estimator_` are, checked on 1.9.1); read the chosen row from `cv_results_`. With `refit=False` none of `best_params_`/`best_estimator_` exist, and multi-metric scoring with the default refit raises `ValueError: For multi-metric scoring, the parameter refit must be set to a scorer key or a callable...`.
- Other uses: constrain by a second metric (best AP subject to recall >= 0.8), or by fit time (`mean_fit_time`).

## Gotchas
- Strings like `"precision"` assume binary labels with positive class `1`; for other labels build `make_scorer(precision_score, pos_label="fraud")`.
- Errors are maximised: losses appear as `neg_*` (e.g. `neg_log_loss`); don't flip signs inconsistently in the refit callable.
- `error_score="raise"` during development so a failing fold doesn't quietly become `nan` and drop out of ranking.

## Verify
- [ ] The refit metric is the business metric, and others are reported alongside.
- [ ] The chosen row's std is examined; differences within one std treated as ties.
- [ ] Final model evaluated once on a held-out test set.
