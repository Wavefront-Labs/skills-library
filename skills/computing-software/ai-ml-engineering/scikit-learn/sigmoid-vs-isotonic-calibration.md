---
id: computing-software.ai-ml-engineering.scikit-learn.sigmoid-vs-isotonic-calibration
name: sigmoid-vs-isotonic-calibration
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, calibration, calibratedclassifiercv, isotonic-calibration, platt-scaling, frozenestimator, probability-calibration]
level: practitioner
status: verified
description: "Calibrate classifier probabilities with CalibratedClassifierCV: sigmoid (Platt) vs isotonic, data size needs, cv vs prefit/FrozenEstimator, and ensemble=True."
sources:
  - https://scikit-learn.org/stable/modules/calibration.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibratedClassifierCV.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.frozen.FrozenEstimator.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sigmoid vs isotonic calibration

**Goal:** turn a classifier's scores into probabilities that match observed frequencies, without leaking or overfitting.

## CalibratedClassifierCV with internal CV
```python
from sklearn.calibration import CalibratedClassifierCV
cal = CalibratedClassifierCV(estimator=HistGradientBoostingClassifier(), method="isotonic", cv=5, ensemble=True)
cal.fit(X_train, y_train)
proba = cal.predict_proba(X_test)[:, 1]
```
- For each fold: fit the estimator on k-1 folds, fit the calibrator on the held-out fold. `ensemble=True` averages the k (estimator, calibrator) pairs at predict time (5 `calibrated_classifiers_` for `cv=5`); `ensemble=False` refits one estimator on all data and uses cross-validated predictions to fit one calibrator (1 entry; faster inference). Test log loss on 6,000 noisy rows: raw 0.492; sigmoid 0.360 (ensemble) / 0.365; isotonic 0.355 / 0.357.

## Already-trained model
Calibrate on a separate calibration set never used for training:
```python
from sklearn.frozen import FrozenEstimator               # scikit-learn >= 1.6
cal = CalibratedClassifierCV(FrozenEstimator(trained_model), method="sigmoid").fit(X_calib, y_calib)
```
(`cv="prefit"` is gone: on 1.9.1 it raises `InvalidParameterError` for `cv`.) The frozen route gave log loss 0.381 against 0.492 for the raw model, with the same ROC-AUC (0.909).

## Sigmoid or isotonic?
| | Sigmoid (Platt) | Isotonic |
|---|---|---|
| Form | 2-parameter logistic on the score | non-parametric monotone step function |
| Data needed | works with a few hundred samples | scikit-learn docs: not recommended well below ~1000 calibration samples (overfits); at 200 rows test log loss was 0.730 for isotonic against 0.380 for sigmoid, at 1,000 rows 0.400 vs 0.381 |
| Fixes | S-shaped distortion (SVMs, boosted trees) | any monotone distortion |
| Ties | none | creates ties (step function): 983 distinct probabilities among 1,500 test rows with `ensemble=True`, only 44 with `ensemble=False`, against 1,500 for sigmoid |
Default to sigmoid for small data; isotonic when you have plenty. Compare both on held-out Brier score/log loss.

## Gotchas
- Calibrating on the training data (same rows the model fitted) does nothing useful; the model is overconfident there (isotonic fitted on the training rows gave test log loss 3.27, against 0.38 when fitted on a separate calibration set).
- Calibration does not change ranking for sigmoid on a single frozen model (monotonic): a `LinearSVC` kept ROC-AUC 0.8691 before and after. With `ensemble=True` the averaged models differ, so AUC can change; it improves log loss/Brier and threshold meaning.
- Class weights distort probabilities (mean prediction 0.311 against a 5.2% base rate with `class_weight="balanced"`, see the calibration-matters skill); calibrate on data with the real class ratio.
- Distribution shift breaks calibration; re-check calibration on recent production data.

## Verify
- [ ] Calibration curve (`CalibrationDisplay`) on held-out data close to the diagonal.
- [ ] Brier score / log loss improved vs uncalibrated.
- [ ] Calibration data disjoint from training data and with the real class prior.
