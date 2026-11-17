---
id: computing-software.ai-ml-engineering.scikit-learn.random-forest-extratrees-and-oob-score
name: random-forest-extratrees-and-oob-score
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, oob-score, extratrees, randomforestclassifier, max-features, bagging]
level: practitioner
status: verified
description: "Tune RandomForest and ExtraTrees in scikit-learn: max_features, min_samples_leaf, n_estimators, oob_score for free validation, and impurity importance pitfalls."
sources:
  - https://scikit-learn.org/stable/modules/ensemble.html#forests-of-randomized-trees
  - https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
  - https://scikit-learn.org/stable/auto_examples/ensemble/plot_ensemble_oob.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RandomForest / ExtraTrees tuning and OOB score

## Parameters that matter (in order)
1. **`max_features`**: features tried per split. Lower = more decorrelated trees. Defaults: `"sqrt"` for classifiers, `1.0` (all) for regressors. Try `sqrt`, `0.3`, `0.5` for regression.
2. **`min_samples_leaf`** (1-20) or **`max_depth`**: regularises noisy data and shrinks model size; default fully-grown trees can be large (100 trees on 2,000 rows pickled to 2.8 MB).
3. **`n_estimators`**: more never overfits, only costs time. Increase until OOB score plateaus (often 200-1000).
4. `max_samples` (bootstrap fraction, e.g. 0.5) speeds training on big data and adds diversity.
5. `class_weight="balanced_subsample"` for imbalance.

## OOB score: free validation
Each tree skips ~37% of rows (1/e = 0.368; (1-1/n)^n = 0.3678 for n=2000); predicting them gives an almost-unbiased estimate without a separate split. On the test data OOB accuracy was 0.913 against 0.906 for 5-fold CV.
```python
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=500, oob_score=True, n_jobs=-1, random_state=0)
rf.fit(X, y); print(rf.oob_score_)                 # accuracy by default; a callable such as `oob_score=f1_score` is accepted (ran: 0.911)
# choose n_estimators cheaply (OOB: 0.9045, 0.909, 0.9125, 0.912, 0.9125 for 50..800 trees in the test):
rf = RandomForestClassifier(warm_start=True, oob_score=True, n_jobs=-1)
for n in [50, 100, 200, 400, 800]:
    rf.set_params(n_estimators=n); rf.fit(X, y); print(n, rf.oob_score_)
```
OOB ignores groups and time: for grouped or temporal data it leaks like random K-fold. Use proper CV there.

## ExtraTrees
`ExtraTreesClassifier` picks split thresholds at random instead of optimally: faster to train, lower variance, sometimes better on noisy or high-dimensional data. Default `bootstrap=False` (so no OOB unless you set `bootstrap=True`; `oob_score=True` without it raises `Out of bag estimation only available if bootstrap=True`). Try both; difference is usually small.

## Importance pitfalls
`feature_importances_` (mean decrease in impurity) is computed on training data and favours high-cardinality and continuous features. In a test with 4 informative features, 6 noise features and a random unique-ID column, the ID column got impurity importance 0.031, the same as the pure-noise columns (0.03 each) and above two of them, but permutation importance on held-out data gave it 0.006 against 0.15-0.17 for the informative features. Use `sklearn.inspection.permutation_importance` on held-out data; correlated features split importance between them.

## Practical notes
- No scaling needed; one-hot or ordinal-encode categoricals (ordinal is fine for trees).
- Missing values: `RandomForestClassifier`, `ExtraTreesClassifier` and `DecisionTreeClassifier` all fitted data containing NaN on 1.9.1; otherwise impute.
- Model size: `min_samples_leaf=5` with 50 trees cut the pickled size from 2.84 MB to 0.84 MB (3.4x) in the test; check the effect on your data with `joblib.dump` size and a CV score.
- Gradient boosting (HistGradientBoosting, LightGBM, XGBoost) is often more accurate on tabular data, but not always: here default RF scored 0.9055 and default HistGradientBoosting 0.9035 in 5-fold CV. RF is a strong, low-tuning baseline. Regression `max_features` test (3 folds): 1.0 and 0.5 gave R2 0.814, 0.3 gave 0.801, `"sqrt"` 0.771.

## Verify
OOB score close to CV score on i.i.d. data; stable when changing `random_state`.
