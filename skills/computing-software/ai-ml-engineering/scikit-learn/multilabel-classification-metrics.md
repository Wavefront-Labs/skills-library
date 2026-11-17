---
id: computing-software.ai-ml-engineering.scikit-learn.multilabel-classification-metrics
name: multilabel-classification-metrics
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, multilabel-metrics, hamming-loss, subset-accuracy, jaccard-score, multilabel-confusion-matrix, multilabel]
level: practitioner
status: verified
description: "Evaluate multilabel classifiers in scikit-learn: subset accuracy, hamming loss, sample/micro/macro F1, jaccard, per-label confusion matrices and ranking metrics."
sources:
  - https://scikit-learn.org/stable/modules/model_evaluation.html#multilabel-ranking-metrics
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.hamming_loss.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.multilabel_confusion_matrix.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multilabel metrics

Targets are a binary indicator matrix `Y (n_samples, n_labels)` (from `MultiLabelBinarizer`). Each sample can have zero or many labels.

## Metrics and what they reward
```python
from sklearn.metrics import accuracy_score, hamming_loss, f1_score, jaccard_score, classification_report
accuracy_score(Y, P)                 # subset accuracy: whole label set must match exactly; very strict
hamming_loss(Y, P)                   # fraction of individual label slots wrong; lenient, dominated by easy negatives
f1_score(Y, P, average="micro")      # pools all label decisions; frequent labels dominate
f1_score(Y, P, average="macro")      # mean per-label F1; rare labels count equally
f1_score(Y, P, average="samples")    # F1 per sample, averaged; "how good is each item's tag set"
jaccard_score(Y, P, average="samples")
print(classification_report(Y, P, target_names=mlb.classes_, zero_division=0))
```
With many labels and sparse positives, hamming loss looks excellent for a model that predicts nothing (1000 samples, 100 labels, one true label each: all-zero predictions give hamming loss 0.01 and samples F1 0.0). Always report a positive-sensitive metric (micro/macro/samples F1) alongside it.

## Per-label confusion
```python
from sklearn.metrics import multilabel_confusion_matrix
mcm = multilabel_confusion_matrix(Y, P)       # (n_labels, 2, 2): [[tn, fp], [fn, tp]] per label
```
Find labels with zero recall or that are never predicted.

## Ranking metrics (from scores, not hard labels)
```python
from sklearn.metrics import label_ranking_average_precision_score, coverage_error, roc_auc_score, average_precision_score
S = clf.predict_proba(X)   # OneVsRestClassifier returns an (n, L) array; MultiOutputClassifier returns a list, see below
label_ranking_average_precision_score(Y, S)
coverage_error(Y, S)                          # how deep in the ranking to go to cover all true labels
average_precision_score(Y, S, average="macro")
```
Note `MultiOutputClassifier.predict_proba` returns a list of `(n, 2)` arrays, one per label (checked on 1.9.1); build `S = np.column_stack([p[:, 1] for p in probas])`.

## Thresholds
Default 0.5 per label is rarely optimal. Tune per-label thresholds on validation data to maximise per-label F1, or a global threshold for micro F1. Also enforce "at least one label" if the product requires it (take the argmax when nothing passes).

## Choosing the headline metric
- Tagging/search: samples F1 or micro F1.
- Rare labels matter (medical codes): macro F1, macro AP.
- Exact set required (configuration): subset accuracy.
