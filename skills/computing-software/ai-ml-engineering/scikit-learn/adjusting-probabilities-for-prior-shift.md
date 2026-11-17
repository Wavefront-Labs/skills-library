---
id: computing-software.ai-ml-engineering.scikit-learn.adjusting-probabilities-for-prior-shift
name: adjusting-probabilities-for-prior-shift
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, prior-shift, label-shift, base-rate, probability-adjustment, calibration, class-prior]
level: practitioner
status: gated
description: "Correct classifier probabilities when the deployment base rate differs from training (prior or label shift): the Bayes prior correction, EM estimation of new priors and checks."
sources:
  - https://direct.mit.edu/neco/article/14/1/21/6556/Adjusting-the-Outputs-of-a-Classifier-to-New-a
  - https://scikit-learn.org/stable/modules/calibration.html
  - https://arxiv.org/abs/1802.03916
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Adjusting probabilities after base-rate (prior) shift

**Prior (label) shift**: class proportions change between training and deployment, while `p(x | y)` stays the same (fraud rate doubles; you undersampled negatives in training). Calibrated probabilities from training then systematically over- or under-estimate.

## Bayes correction (known priors)
For training priors `pi_train[k]` and deployment priors `pi_new[k]`:
```python
def adjust(proba, pi_train, pi_new):
    w = np.asarray(pi_new) / np.asarray(pi_train)
    p = proba * w
    return p / p.sum(axis=1, keepdims=True)
```
Binary odds form: `odds_new = odds_model * (pi_new / (1 - pi_new)) / (pi_train / (1 - pi_train))`.
- Classic use: after undersampling negatives by factor r, the positive prior in training is inflated; correct back to the real base rate (this is the same as `p / (p + (1 - p) / beta)` with beta the sampling rate of negatives).
- Apply on **calibrated** probabilities; correction assumes the model estimates `p(y|x)` under training priors well.

## Unknown new priors: estimate them
EM prior estimation (Saerens, Latinne and Decaestecker, Neural Computation 2002; authorship unconfirmed, gated: unconfirmed, source is paywalled or blocked) on unlabelled deployment data (the code below converged to priors 0.902/0.098 against a true 0.900/0.100 in a test):
```python
def em_priors(proba, pi_train, iters=100, tol=1e-6):
    pi = np.asarray(pi_train, float)
    for _ in range(iters):
        p = adjust(proba, pi_train, pi)
        new = p.mean(axis=0)
        if np.abs(new - pi).max() < tol: break
        pi = new
    return pi
```
Alternative: Black Box Shift Estimation (BBSE) using the confusion matrix on validation data (Lipton et al. 2018), more robust when the model is miscalibrated.

## What changes and what does not
- Ranking (ROC AUC) is unchanged by prior shift: no adjustment needed for pure ranking.
- Thresholds and expected-value decisions do change: re-derive the threshold from adjusted probabilities and costs.
- Precision changes with base rate even at fixed TPR/FPR; report precision at the deployment prior.

## Detect it
Compare average predicted probability on recent unlabelled data with the training prior, and once labels arrive, the observed rate. A persistent gap with stable feature distributions suggests prior shift; feature drift too suggests covariate or concept shift, which this correction does not fix.

## Verify
On a validation set resampled to the new prior, log loss/Brier should improve after adjustment.
