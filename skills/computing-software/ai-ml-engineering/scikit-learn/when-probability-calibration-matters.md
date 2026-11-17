---
id: computing-software.ai-ml-engineering.scikit-learn.when-probability-calibration-matters
name: when-probability-calibration-matters
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, calibration, calibration-need, predict-proba, naive-bayes, svm-probability, random-forest-calibration, decision-making]
level: practitioner
status: verified
description: "Decide whether a model needs calibration: which classifiers are miscalibrated and why, which uses need true probabilities, and what class weights do to them."
sources:
  - https://scikit-learn.org/stable/modules/calibration.html
  - https://scikit-learn.org/stable/auto_examples/calibration/plot_compare_calibration.html
  - https://www.cs.cornell.edu/~alexn/papers/calibration.icml05.crc.rev3.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# When probability calibration matters

**Goal:** spend effort on calibration exactly when the downstream use depends on probabilities being right.

## Uses that need calibrated probabilities
- Expected-value decisions: `p(default) x loss` for pricing, provisioning, bidding.
- Comparing or combining scores across models/segments (one threshold for all regions).
- Showing probabilities to people (risk scores, "80% likely").
- Feeding probabilities into another model or a simulation.

## Uses that don't
- Pure ranking (top-k lead lists, search ordering): ROC-AUC and ranking are unchanged by monotone calibration.
- A single threshold tuned directly on validation data for one business metric (the threshold absorbs miscalibration) - as long as the class prior doesn't shift.

## Typical behaviour by model (Niculescu-Mizil & Caruana, 2005; scikit-learn docs)
| Model | Typical calibration |
|---|---|
| `LogisticRegression` (unpenalised or mild penalty) | well calibrated when the model form fits (optimises log loss directly); on noisy non-linear synthetic data its quantile-bin calibration gap was still 0.056 |
| Gaussian Naive Bayes | over-confident, pushes probabilities to 0/1 (independence assumption): 17% of test predictions beyond 0.02/0.98 against 5% for logistic regression, log loss 0.504 vs 0.423 |
| Random forest | under-confident near extremes on noisy data: predictions ranged only 0.01 to 0.995 and 0.7% were beyond 0.02/0.98 (this depends on the data: on an easy, nearly noise-free dataset the same forest output exactly 0 and 1) |
| SVM (`decision_function`) | not probabilities; `SVC(probability=True)` (deprecated since scikit-learn 1.9, removal in 1.11; use `CalibratedClassifierCV(SVC(), ensemble=False)`) runs internal Platt scaling with 5-fold CV (slow, and disagreed with `predict` on 0.3% of rows) |
| Gradient boosting with log loss | usually decent; degrades with many trees / high learning rate: 100 default iterations gave gap 0.022 and log loss 0.327, 1000 iterations at learning rate 0.3 without early stopping gave gap 0.085, log loss 0.831 and 89% of predictions beyond 0.02/0.98 |
| Deep nets | often over-confident (Guo et al., 2017) |

## Things that break calibration
- Class weights (`class_weight="balanced"`): the model learns a different prior; probabilities are inflated for the minority class (5.2% positives: mean predicted probability 0.055 unweighted, 0.311 with `class_weight="balanced"`).
- Strong regularisation (pulls probabilities toward 0.5): the standard deviation of predicted probabilities was 0.155 at `C=1e-4` against 0.333 at `C=1`.
- Prior shift in production: base rate changes from 2% to 5% and every probability is off. Re-calibrate or apply a prior correction `odds_new = odds_old x (prior_new/(1-prior_new)) / (prior_train/(1-prior_train))` (test: training prior 5.2%, test set resampled to 20% positives; mean prediction 0.105 uncorrected, 0.207 corrected, Brier score 0.103 to 0.088).

## Quick check
```python
from sklearn.calibration import CalibrationDisplay
CalibrationDisplay.from_estimator(model, X_val, y_val, n_bins=10, strategy="quantile")
```
Plus Brier score vs a calibrated variant. If the curve hugs the diagonal and Brier doesn't improve with calibration, skip it.

## Verify
- [ ] Downstream use classified as probability-dependent or ranking-only.
- [ ] Calibration curve checked on held-out data with the production class prior.
- [ ] Any class weighting followed by recalibration.
