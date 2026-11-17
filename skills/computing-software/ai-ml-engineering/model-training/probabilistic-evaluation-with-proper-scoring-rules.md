---
id: computing-software.ai-ml-engineering.model-training.probabilistic-evaluation-with-proper-scoring-rules
name: probabilistic-evaluation-with-proper-scoring-rules
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, proper-scoring-rules, log-loss, brier-score, crps, calibration, probabilistic-forecasting]
level: practitioner
status: verified
description: "Evaluate probabilistic predictions with proper scoring rules: log loss, Brier and its decomposition, CRPS and pinball loss, reliability diagrams and skill scores."
sources:
  - https://doi.org/10.1198/016214506000001437
  - https://scikit-learn.org/stable/modules/model_evaluation.html#probabilistic-predictions
  - https://github.com/properscoring/properscoring
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Probabilistic evaluation with proper scoring rules

A scoring rule is **proper** if a forecaster minimises expected loss by reporting their true belief; **strictly proper** if that minimum is unique (Gneiting and Raftery 2007). Accuracy, F1 and AUC are not proper scores for probabilities: they can be gamed or ignore calibration.

## Classification
| Score | Formula | Notes |
|---|---|---|
| Log loss | `-log p(y)` | strictly proper; punishes confident errors heavily; local |
| Brier | `mean((p - y)^2)` (sum over classes for multiclass; `sklearn.metrics.brier_score_loss` accepted 3-class probabilities on 1.9.1 and returned 0.1467 = that sum averaged over samples) | strictly proper; bounded; decomposes |
| Spherical | `p(y) / ||p||` | rarely used |

Brier decomposition (Murphy): `Brier = reliability - resolution + uncertainty`. Reliability = calibration error (lower is better), resolution = how much forecasts vary with outcome (higher is better), uncertainty = base rate variance (fixed by data).

## Regression / distributions
- **CRPS** (continuous ranked probability score): compares the full predictive CDF with the outcome; reduces to MAE for point forecasts, so it is in target units. `properscoring.crps_gaussian(x, mu, sig)` (the third argument is named `sig`, not `sigma`) or `crps_ensemble(observations, forecasts)`; tested that `crps_ensemble(0.5, [1.5])` returns 1.0, the absolute error.
- **Pinball (quantile) loss** for each predicted quantile; average over quantiles approximates CRPS. `sklearn.metrics.mean_pinball_loss(y, q_pred, alpha=0.9)` (ran).
- **Negative log-likelihood** of the predictive distribution (Gaussian NLL etc.); proper but sensitive to tail misspecification.
- Interval forecasts: interval score (Winkler) penalises width plus misses.

## Skill scores
Compare to a reference forecast (climatology / prior rates / naive): `skill = 1 - score_model / score_reference`. Positive = better than baseline. Always report the baseline.

## Diagnostics alongside scores
- Reliability diagram (`CalibrationDisplay.from_predictions(y, p, n_bins=10, strategy="quantile")`, ran).
- For distributions: PIT histogram (probability integral transform `F(y)` should be uniform) and empirical coverage of prediction intervals (90% intervals should contain ~90% of outcomes).
- Sharpness: among calibrated forecasts, narrower (more confident) is better.

## Practice
- Select models and early-stop on a proper score when probabilities feed decisions.
- Compare scores with paired tests or bootstrap over the same test examples; differences are often small in absolute terms.
- ECE (expected calibration error) is a diagnostic, not a proper score; do not optimise it alone.
