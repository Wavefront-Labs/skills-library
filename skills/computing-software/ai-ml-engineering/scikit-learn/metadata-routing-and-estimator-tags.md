---
id: computing-software.ai-ml-engineering.scikit-learn.metadata-routing-and-estimator-tags
name: metadata-routing-and-estimator-tags
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, metadata-routing, set-fit-request, sample-weight-routing, estimator-tags, sklearn-tags, sklearn-api-contract]
level: practitioner
status: verified
description: "Route sample_weight, groups and other metadata through pipelines and searches with scikit-learn metadata routing, and declare estimator capabilities via tags."
sources:
  - https://scikit-learn.org/stable/metadata_routing.html
  - https://scikit-learn.org/stable/auto_examples/miscellaneous/plot_metadata_routing.html
  - https://scikit-learn.org/stable/developers/develop.html#estimator-tags
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metadata routing and estimator tags

**Goal:** pass `sample_weight`, `groups` or custom metadata to exactly the steps that should receive them inside `Pipeline`, `GridSearchCV` and `cross_validate`.

## The problem
Old style: `pipe.fit(X, y, clf__sample_weight=w)` works for pipelines. Without routing, `GridSearchCV.fit(X, y, sample_weight=w)` on 1.9.1 passed the weights to both the estimator and the `accuracy` scorer (`best_score_` 0.9173 equalled the hand-computed weighted accuracy, not the unweighted 0.9267), so you cannot send them to only one of the two, nor give two pipeline steps different arrays. Metadata routing makes every consumer declare what it wants.

## Turn it on
```python
import sklearn
sklearn.set_config(enable_metadata_routing=True)
```

## Request metadata per consumer
```python
from sklearn.metrics import make_scorer, roc_auc_score
clf = LogisticRegression().set_fit_request(sample_weight=True)
scorer = make_scorer(roc_auc_score, response_method="predict_proba").set_score_request(sample_weight=True)
scaler = StandardScaler().set_fit_request(sample_weight=False)       # explicit: don't use weights here
pipe = make_pipeline(scaler, clf)

search = GridSearchCV(pipe, {"logisticregression__C": [0.1, 1, 10]}, scoring=scorer, cv=GroupKFold(5))
search.fit(X, y, sample_weight=w, groups=g)   # groups go to the CV splitter, weights to clf and scorer
```
`cross_validate(pipe, X, y, params={"sample_weight": w, "groups": g}, cv=GroupKFold(5), scoring=scorer)` - note `params=`, not the old `fit_params=` (`fit_params` raises `TypeError: ... unexpected keyword argument` on 1.9.1).

- If metadata is passed but a consumer's request isn't set, scikit-learn raises `UnsetMetadataPassedError: [sample_weight] are passed but are not explicitly set as requested or not requested for StandardScaler.fit_transform, which is used within Pipeline.fit. Call StandardScaler.set_fit_request(...)...`; decide with `True`, `False`, or an alias string. That error is the point: no silent dropping. (`GridSearchCV` wraps it in `ValueError: All the N fits failed` unless `error_score="raise"`.)
- Aliases: `set_fit_request(sample_weight="fit_w")` lets two steps get different weight arrays.
- Check routing support per estimator in the docs; third-party estimators may not implement it yet.

## Estimator tags
Tags tell scikit-learn (and its test suite) what an estimator supports: NaN input, sparse input, positive-only data, multi-output, requires `y`, and so on. In >= 1.6:
```python
def __sklearn_tags__(self):
    tags = super().__sklearn_tags__()
    tags.input_tags.allow_nan = True
    tags.input_tags.sparse = True
    return tags
```
(Older releases used `_more_tags()` returning a dict; on 1.9.1 a `_more_tags` method is ignored, e.g. `get_tags(est).input_tags.allow_nan` stays False.) `check_estimator` uses tags to pick which checks run; inspect them with `sklearn.utils.get_tags(est)`.

## Verify
- [ ] With routing enabled, scorer receives weights (weighted vs unweighted CV scores differ as expected).
- [ ] `groups` reach the splitter inside nested searches.
- [ ] Custom estimator tags reflect its real capabilities and `check_estimator` passes.
