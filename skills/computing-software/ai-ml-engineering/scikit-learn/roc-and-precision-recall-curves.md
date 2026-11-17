---
id: computing-software.ai-ml-engineering.scikit-learn.roc-and-precision-recall-curves
name: roc-and-precision-recall-curves
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, roc-curve, precision-recall-curve, roccurvedisplay, average-precision, auc]
level: practitioner
status: verified
description: "Compute and plot ROC and precision-recall curves with RocCurveDisplay/PrecisionRecallDisplay, pick operating points from thresholds, and know when PR beats ROC."
sources:
  - https://scikit-learn.org/stable/modules/model_evaluation.html#roc-metrics
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html
  - https://scikit-learn.org/stable/visualizations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ROC and precision-recall curves

## Compute
```python
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score
scores = clf.predict_proba(X_test)[:, 1]          # or decision_function
fpr, tpr, roc_thr = roc_curve(y_test, scores)
prec, rec, pr_thr = precision_recall_curve(y_test, scores)
print(roc_auc_score(y_test, scores), average_precision_score(y_test, scores))
```
Use continuous scores, not hard predictions; `predict` output gives a single point.

## Plot (Display API)
```python
from sklearn.metrics import RocCurveDisplay, PrecisionRecallDisplay
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
RocCurveDisplay.from_estimator(clf, X_test, y_test, ax=ax[0], plot_chance_level=True)
PrecisionRecallDisplay.from_predictions(y_test, scores, ax=ax[1], plot_chance_level=True)
```
Overlay several models by reusing the same axes. `RocCurveDisplay.from_cv_results(cv_results, X, y)` plots fold curves (ran with `cross_validate(..., return_estimator=True, return_indices=True)`).

## ROC vs PR
- ROC (TPR vs FPR) is insensitive to class prevalence; with 0.1% positives, a model can have 0.98 ROC-AUC and still produce mostly false alarms (test with 0.1% positives: ROC-AUC 0.990, average precision 0.438; at 90% recall precision was 0.054, and flagging the top 5% of scores gave precision 0.018).
- PR curves expose precision at each recall; the no-skill baseline is the positive rate. Prefer PR/average precision for rare positives and retrieval-like tasks.
- `average_precision_score` (step-wise) is preferred over trapezoidal `auc(rec, prec)`, which can be optimistic (the docs warn about linear interpolation; in the test the trapezoid gave 0.424 against AP 0.438, so it is not always higher).

## Choosing an operating point
```python
target_recall = 0.9
i = np.where(rec[:-1] >= target_recall)[0][-1]       # thresholds has len(rec) - 1 (10,000 vs 10,001 in the test)
print("threshold", pr_thr[i], "precision", prec[i])
```
Or Youden's J on ROC (`argmax(tpr - fpr)`), or cost-based selection with `TunedThresholdClassifierCV`. Choose thresholds on validation data, then report test performance at that fixed threshold.

## Multiclass
One-vs-rest curves per class (`label_binarize`) or `roc_auc_score(y, proba, multi_class="ovr", average="macro")`.

## Verify
- [ ] Curves plotted with chance levels; chosen threshold and its precision/recall reported on the test set.
