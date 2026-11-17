---
id: computing-software.ai-ml-engineering.scikit-learn.multiclass-averaging-and-classification-report
name: multiclass-averaging-and-classification-report
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, macro-average, classification-report, micro-average, weighted-average, multiclass-metrics]
level: practitioner
status: verified
description: "Read multiclass and multilabel metrics in scikit-learn: macro, micro, weighted and samples averaging, classification_report, confusion matrices and ROC AUC OvR/OvO."
sources:
  - https://scikit-learn.org/stable/modules/model_evaluation.html#multiclass-and-multilabel-classification
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiclass averaging and classification_report

## Averages
| `average=` | Computes | Use when |
|---|---|---|
| `"macro"` | unweighted mean of per-class scores | every class matters equally, including rare ones |
| `"weighted"` | mean weighted by class support | summary that follows class frequencies; can hide rare-class failure |
| `"micro"` | pool all TP/FP/FN globally | overall performance; for single-label multiclass, micro P = R = F1 = accuracy |
| `"samples"` | per-sample then mean (multilabel only; raises `Samplewise metrics are not available outside of multilabel classification` on single-label y) | multilabel set-based quality |
| `None` | per-class array | to see where the model fails |

## classification_report
```python
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
print(classification_report(y_true, y_pred, labels=labels, target_names=names, digits=3, zero_division=0))
ConfusionMatrixDisplay.from_predictions(y_true, y_pred, normalize="true", xticks_rotation=45)
```
- Rows report precision, recall, F1 and support per class, then accuracy, macro avg, weighted avg.
- `zero_division=0` silences the warning (`Precision is ill-defined and being set to 0.0 due to no predicted samples`) when a class is never predicted (precision undefined); a 0 there means the model never predicts that class, or the class is absent from `y_true`: investigate.
- Pass `labels=` to include classes absent from this split, so reports are comparable across folds. Absent classes get precision/recall/F1 of 0 and support 0 and are included in the macro average: on a 4-class problem adding a fifth, never-seen label dropped macro F1 from 0.485 to 0.388 (weighted avg unchanged at 0.698), so only list labels that can occur.
- `normalize="true"` on the confusion matrix shows recall per row; easier to read than raw counts with imbalance.

## Probability metrics
```python
roc_auc_score(y_true, proba, multi_class="ovr", average="macro")   # one-vs-rest
roc_auc_score(y_true, proba, multi_class="ovo", average="macro")   # one-vs-one, insensitive to imbalance
log_loss(y_true, proba, labels=clf.classes_)
top_k_accuracy_score(y_true, proba, k=3, labels=clf.classes_)
```
`proba` columns must follow `clf.classes_` order.

## Multilabel
`y` is a binary indicator matrix (`MultiLabelBinarizer`). Use `f1_score(Y, Yp, average="samples")`, `hamming_loss`, `jaccard_score`; per-label thresholds usually beat a global 0.5.

## Choosing the headline metric
- Imbalanced classes where minority matters: macro-F1 or macro-recall (balanced accuracy = macro recall).
- Ranking/probability quality: log loss, macro AUC.
- Report per-class numbers alongside any average; a single average hides which classes fail.
- In CV, compute macro scores per fold and average; micro-pooling predictions across folds gives a different number (state which).

## Verify
For single-label multiclass, check `f1_score(average="micro") == accuracy_score`; if not, labels are misaligned or it's actually multilabel.
