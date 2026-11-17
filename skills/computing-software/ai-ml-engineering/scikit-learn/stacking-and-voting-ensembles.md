---
id: computing-software.ai-ml-engineering.scikit-learn.stacking-and-voting-ensembles
name: stacking-and-voting-ensembles
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, stackingclassifier, voting-classifier, stackingregressor, ensemble, meta-learner]
level: practitioner
status: verified
description: "Combine models in scikit-learn with VotingClassifier and StackingClassifier/Regressor: soft vs hard voting, out-of-fold meta-features, passthrough and leakage-safe CV."
sources:
  - https://scikit-learn.org/stable/modules/ensemble.html#voting-classifier
  - https://scikit-learn.org/stable/modules/ensemble.html#stacked-generalization
  - https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.StackingClassifier.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stacking and voting ensembles

Ensembles help when base models are good and make different errors (e.g. a linear model, a GBM, a kNN). Combining near-identical models adds cost, not accuracy.

## Voting
```python
from sklearn.ensemble import VotingClassifier
from sklearn.calibration import CalibratedClassifierCV
vote = VotingClassifier(
    estimators=[("lr", make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))),
                ("hgb", HistGradientBoostingClassifier()),
                ("svc", make_pipeline(StandardScaler(), CalibratedClassifierCV(SVC(), ensemble=False)))],
    voting="soft", weights=[1, 2, 1], n_jobs=-1)
```
- `soft` averages `predict_proba`: usually better than `hard` (majority vote) if models are reasonably calibrated (accuracy 0.883 soft vs 0.876 hard in a 5-fold test). `SVC(probability=True)` is deprecated since 1.9 (removal in 1.11, FutureWarning recommending `CalibratedClassifierCV(SVC(), ensemble=False)`), so the SVC step above uses that; it ran inside `VotingClassifier`. Gains are not guaranteed: soft voting reached ROC-AUC 0.945 against 0.949 for the best single model (`HistGradientBoostingClassifier`) in the same folds.
- Weights by validation performance; don't tune weights on the test set.
- `VotingRegressor` averages predictions.

## Stacking
```python
from sklearn.ensemble import StackingClassifier
stack = StackingClassifier(
    estimators=[("lr", ...), ("hgb", ...), ("knn", make_pipeline(StandardScaler(), KNeighborsClassifier(25)))],
    final_estimator=LogisticRegression(C=1.0), cv=5, stack_method="auto", passthrough=False, n_jobs=-1)
stack.fit(X_train, y_train)
```
- Base models' **out-of-fold** predictions (internal `cv`) train the final estimator, so the meta-learner never sees predictions on rows a base model was fit on. Manual stacking that fits bases on all training data then trains the meta-model on those in-sample predictions leaks and overweights overfit models.
- After building meta-features, each base model is refit on the full training set for prediction.
- Keep the final estimator simple (regularised logistic/ridge). A GBM on top overfits easily.
- `passthrough=True` also feeds original features to the meta-learner; helps sometimes, overfits often.
- For grouped data, `StackingClassifier(cv=GroupKFold(3)).fit(X, y, groups=g)` fails on 1.9.1: without routing it raises `ValueError: Passing extra keyword arguments to StackingClassifier.fit is only supported if enable_metadata_routing=True`, and with routing enabled `TypeError: fit got unexpected argument(s) {'groups'}, which are not routed to any object`. What worked: pass pre-computed splits, `cv=list(GroupKFold(3).split(X, y, g))`. For time series, `cv=TimeSeriesSplit(3)` raises `ValueError: cross_val_predict only works for partitions`; build OOF predictions manually with `TimeSeriesSplit` (and drop the first fold).

## Evaluate fairly
Wrap the whole stack in outer CV (`cross_val_score(stack, X, y, cv=outer)`): costly (bases x inner folds x outer folds) but the only honest estimate. Compare with the best single base model; gains of 0.5-2% AUC are typical, sometimes none.

## Costs
Inference latency and maintenance multiply by the number of bases. For production, check whether the gain justifies it, or distil the ensemble into one model.

## Verify
`stack.final_estimator_.coef_` shows how much each base contributes; a base with ~0 weight can be dropped (in the test, with LR, HGB and kNN bases the weights were 0.04, 3.37 and 3.38 on probability columns; in the same 5-fold run the stack scored ROC-AUC 0.9493 against 0.9491 for HGB alone, a negligible gain). `passthrough=True` made the final estimator see 14 inputs (2 base-model columns plus the 12 original features) instead of 2.
