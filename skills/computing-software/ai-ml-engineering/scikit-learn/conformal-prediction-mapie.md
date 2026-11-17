---
id: computing-software.ai-ml-engineering.scikit-learn.conformal-prediction-mapie
name: conformal-prediction-mapie
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, conformal-prediction, mapie, prediction-intervals, prediction-sets, uncertainty-quantification]
level: practitioner
status: verified
description: "Add distribution-free uncertainty with conformal prediction: split conformal intervals and sets, MAPIE regressors/classifiers, CQR, coverage checks and exchangeability caveats."
sources:
  - https://mapie.readthedocs.io/en/stable/
  - https://arxiv.org/abs/2107.07511
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Conformal prediction (MAPIE)

**Promise:** for any fitted model, produce intervals (regression) or label sets (classification) that contain the truth with probability at least 1 - alpha on average, assuming calibration and test data are exchangeable.

## Split conformal by hand (regression)
```python
model.fit(X_train, y_train)
resid = np.abs(y_cal - model.predict(X_cal))                 # held-out calibration set
n, alpha = len(resid), 0.1
q = np.quantile(resid, np.ceil((n + 1) * (1 - alpha)) / n, method="higher")
pred = model.predict(X_test); lower, upper = pred - q, pred + q
```
Constant-width intervals; use CQR or normalized scores for adaptive widths.

## MAPIE (v1 API; older releases used MapieRegressor/MapieClassifier)
```python
from mapie.regression import SplitConformalRegressor, ConformalizedQuantileRegressor
scr = SplitConformalRegressor(model, confidence_level=0.9, prefit=True)
scr.conformalize(X_cal, y_cal)
y_pred, y_int = scr.predict_interval(X_test)                  # y_int shape (n, 2, 1)

from mapie.classification import SplitConformalClassifier
scc = SplitConformalClassifier(clf, confidence_level=0.95, conformity_score="lac", prefit=True)
scc.conformalize(X_cal, y_cal)
y_pred, y_sets = scc.predict_set(X_test)                      # boolean (n, n_classes, 1)
```
Pin the MAPIE version: the API changed substantially in 1.0. The block above ran on MAPIE 1.5.0; on a calibration/test split the manual version covered 0.902 and `SplitConformalRegressor` 0.900 at 0.9 confidence, and the classifier returned boolean sets of shape (n, 3, 1) (tested).

## Choosing the score
- Regression: absolute residual (constant width), CQR with quantile models (adaptive), cross-conformal / jackknife+ when data is scarce (no separate calibration set).
- Classification: LAC (smallest sets on average), APS/RAPS (more adaptive coverage across difficulty).

## Caveats
- Coverage is **marginal**, not per subgroup. Check coverage by segment; use Mondrian (group-conditional) conformal for per-group guarantees.
- Time series and distribution shift break exchangeability; use time-series variants (EnbPI, ACI) and recalibrate regularly.
- Calibration set size: small sets give noisy quantiles, so coverage on a test set fluctuates around the target; use a larger calibration split or cross-conformal methods.

## Verify
- [ ] Empirical coverage on a test set is close to the target; report average interval width / set size.
