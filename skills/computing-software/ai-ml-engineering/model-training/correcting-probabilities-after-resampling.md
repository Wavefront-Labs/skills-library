---
id: computing-software.ai-ml-engineering.model-training.correcting-probabilities-after-resampling
name: correcting-probabilities-after-resampling
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, resampling-calibration, undersampling, oversampling, smote, prior-correction, calibration]
level: practitioner
status: gated
description: "Undo the probability distortion caused by undersampling, oversampling, SMOTE or class weights: analytic prior correction, recalibration on untouched data, new thresholds."
sources:
  - https://www3.nd.edu/~dial/publications/dalpozzolo2015calibrating.pdf
  - https://scikit-learn.org/stable/modules/calibration.html
  - https://imbalanced-learn.org/stable/common_pitfalls.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Correcting probabilities after resampling

Rebalancing the training data (random undersampling, oversampling, SMOTE) or using `class_weight="balanced"` makes the model believe positives are much more common. Its probabilities are inflated for the positive class. Ranking may be fine; probabilities and thresholds are not.

## Analytic correction for undersampling
If negatives were kept with probability `beta` (e.g. 0.1) and positives all kept, the model's `p_s` relates to the true `p` by (Dal Pozzolo et al. 2015):
```python
def undo_undersampling(p_s, beta):
    return beta * p_s / (beta * p_s - p_s + 1)
```
Tested on 100k simulated rows (true positive rate 5.7%, beta = 0.1): the undersampled model predicted a mean of 0.251, the corrected mean was 0.058, and log loss fell from 0.344 to 0.158.
For class weights `w_pos`, `w_neg`, the equivalent is a prior shift with odds multiplied by `w_pos / w_neg`: divide the model odds by that ratio.
```python
def undo_weights(p, w_pos, w_neg):
    odds = p / (1 - p) * (w_neg / w_pos)
    return odds / (1 + odds)
```
Tested with `class_weight={0: 1, 1: 10}`: mean prediction 0.249 before, 0.058 after, against a true rate of 0.057.

## SMOTE and complex resampling
No exact formula (synthetic points change `p(x|y)` too). Recalibrate empirically:
```python
from sklearn.calibration import CalibratedClassifierCV
# model trained on resampled data inside an imblearn Pipeline
from sklearn.frozen import FrozenEstimator            # scikit-learn 1.6+
cal = CalibratedClassifierCV(FrozenEstimator(fitted_pipe), method="isotonic")   # cv="prefit" raises InvalidParameterError on 1.9.1 (tested)
cal.fit(X_cal, y_cal)          # untouched, original-distribution calibration set
```
Use `method="sigmoid"` if the calibration set is small; isotonic overfits small sets (the ~1000 threshold sometimes quoted is a heuristic (gated: unconfirmed, source is paywalled or blocked)). With FrozenEstimator the calibrated mean was 0.0565 against a true rate of 0.0578 (tested).

## Rules
- Resample **only the training folds**, never validation/test/calibration data. Use `imblearn.pipeline.Pipeline` so resampling happens inside each CV fold.
- Evaluate log loss / Brier / reliability on original-distribution data after correction.
- Re-derive the decision threshold from corrected probabilities and costs (e.g. `t = c_fp / (c_fp + c_fn)`), or tune it directly on validation with `TunedThresholdClassifierCV`.

## Often better: do not resample
Gradient boosting and logistic regression trained on the original distribution usually rank as well as resampled versions, with calibrated probabilities for free; handle imbalance with threshold choice and evaluation metrics. Resample when training cost or a specific model needs it, then correct.

## Verify
Mean predicted probability on the test set should be close to the observed positive rate after correction; check a reliability diagram.
