---
id: computing-software.ai-ml-engineering.scikit-learn.bagging-and-adaboost-ensembles
name: bagging-and-adaboost-ensembles
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, baggingclassifier, adaboost, bagging, boosting, ensemble-methods, out-of-bag]
level: practitioner
status: verified
description: "Use scikit-learn BaggingClassifier/Regressor and AdaBoost: base estimators, max_samples/max_features, OOB scoring, learning_rate vs n_estimators and when GBMs win."
sources:
  - https://scikit-learn.org/stable/modules/ensemble.html#bagging-meta-estimator
  - https://scikit-learn.org/stable/modules/ensemble.html#adaboost
  - https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BaggingClassifier and AdaBoost

## Bagging: reduce variance of unstable models
```python
from sklearn.ensemble import BaggingClassifier
bag = BaggingClassifier(estimator=DecisionTreeClassifier(), n_estimators=200,
                        max_samples=0.8, max_features=0.8, bootstrap=True, bootstrap_features=False,
                        oob_score=True, n_jobs=-1, random_state=0).fit(X, y)
bag.oob_score_
```
- Helps high-variance learners (deep trees, KNN, small neural nets); does little for stable models (linear regression).
- `max_features < 1` = random subspaces; `bootstrap=False, max_samples<1` = pasting.
- `oob_score_` is a free validation estimate when bootstrapping (each estimator skips about 37% of rows, (1 - 1/n)^n, computed 0.368 for n=1000).
- With trees, `RandomForestClassifier` is usually better (per-split feature sampling) and faster; use Bagging when the base model is not a tree or you need custom estimators.

## AdaBoost: reweight hard examples
```python
from sklearn.ensemble import AdaBoostClassifier
ada = AdaBoostClassifier(estimator=DecisionTreeClassifier(max_depth=1), n_estimators=300, learning_rate=0.5, random_state=0)
```
- Weak learners: stumps or shallow trees (depth 1-3). Deep trees overfit quickly.
- `learning_rate` and `n_estimators` trade off: smaller rate needs more estimators. Tune with `staged_predict` / `staged_score` to see validation score per iteration without refitting:
```python
scores = [accuracy_score(y_val, p) for p in ada.fit(X_tr, y_tr).staged_predict(X_val)]
```
- Only the SAMME algorithm remains: in scikit-learn 1.9.1 `AdaBoostClassifier` has no `algorithm` argument at all (`AdaBoostClassifier(algorithm="SAMME.R")` raises `TypeError: unexpected keyword argument`, tested). On older releases pass nothing or `algorithm="SAMME"`.
- Sensitive to label noise and outliers (it keeps upweighting them). Clean labels first.
- `AdaBoostRegressor` uses AdaBoost.R2 with `loss="linear"|"square"|"exponential"`.

## When gradient boosting wins
`HistGradientBoostingClassifier`, XGBoost, LightGBM generally beat AdaBoost on tabular data with less tuning, handle missing values and scale better. AdaBoost remains useful as a teaching model, with custom weak learners, or when you need a very small model of stumps.

## Imbalanced data
Plain bagging on imbalanced data inherits the imbalance. Use `imblearn.ensemble.BalancedBaggingClassifier` / `RUSBoostClassifier` or class weights in the base estimator.

## Verify
Compare against the single base estimator and a RandomForest/HistGradientBoosting baseline with the same CV; ensembles should beat the single model clearly or are not worth the cost.
