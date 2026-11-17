---
id: computing-software.ai-ml-engineering.scikit-learn.log-loss-and-proper-scoring
name: log-loss-and-proper-scoring
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, log-loss, cross-entropy, brier-score, proper-scoring-rules, probability-evaluation, calibration]
level: practitioner
status: verified
description: "Evaluate predicted probabilities with scikit-learn log_loss and brier_score_loss: interpretation, clipping, multiclass labels, baselines and why accuracy hides bad probabilities."
sources:
  - https://scikit-learn.org/stable/modules/model_evaluation.html#log-loss
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html
  - https://scikit-learn.org/stable/modules/model_evaluation.html#brier-score-loss
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Log loss and proper scoring of probabilities

**Log loss** (cross-entropy): `-mean(log p(true class))`. It is a strictly proper scoring rule: the expected score is optimal only when predicted probabilities equal true probabilities, so it rewards honest probabilities, not just correct rankings.

```python
from sklearn.metrics import log_loss, brier_score_loss
proba = clf.predict_proba(X_test)
log_loss(y_test, proba, labels=clf.classes_)             # pass labels if some classes are missing from y_test
brier_score_loss(y_test, proba[:, 1], pos_label=1)       # binary: mean squared error of probabilities
```
Scoring strings: `"neg_log_loss"`, `"neg_brier_score"` (negated so higher is better in CV/search).

## Interpreting values
- Baseline: predicting class frequencies `p_k` gives log loss = entropy of labels: `-sum p_k log p_k`. Binary 50/50 = 0.693; 90/10 = 0.325. A model must beat this to have any skill.
```python
prior = np.bincount(y_train) / len(y_train)
log_loss(y_test, np.tile(prior, (len(y_test), 1)))
```
- One confident wrong prediction (p=0.0001 for the true class) adds `-log(1e-4)/n = 9.2/n`. Log loss punishes overconfidence harshly; Brier is bounded and gentler.
- Log loss uses natural log in scikit-learn.

## Clipping
Probabilities of exactly 0 for the true class give infinite loss; scikit-learn clips to machine epsilon (2.2e-16) internally (the `eps` parameter is gone in 1.9.1; the signature is `log_loss(y_true, y_proba=None, *, normalize=True, sample_weight=None, labels=None, y_pred='deprecated')`). If your model outputs hard 0/1, log loss will be huge: that is a correct verdict on its probabilities.

## Multiclass
`proba` must be `(n_samples, n_classes)` with columns in `clf.classes_` order; rows must sum to 1. If they do not, scikit-learn only warns (`The y_prob values do not sum to one`) and scores the raw values without renormalising (checked on 1.9.1), so normalise first. If `y_true` holds a single class, pass `labels=` or it raises `ValueError`.

## Use with other metrics
- Accuracy/F1 measure decisions at a threshold; ROC AUC measures ranking; log loss/Brier measure probability quality. A model can have better AUC and worse log loss (miscalibrated).
- Brier decomposes into calibration + refinement; pair with a reliability diagram (`CalibrationDisplay`).
- Tune early stopping and model selection on log loss when downstream uses probabilities (pricing, expected value, risk).

## Verify
Compare model log loss to the prior baseline and after `CalibratedClassifierCV`; if calibration improves log loss a lot, the raw model was miscalibrated.
