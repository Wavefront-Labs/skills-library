---
id: computing-software.ai-ml-engineering.model-training.confusion-matrix-and-worst-error-analysis
name: confusion-matrix-and-worst-error-analysis
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, error-analysis, confusion-matrix-analysis, worst-errors, error-buckets, model-debugging]
level: practitioner
status: draft
description: "Run structured error analysis: normalized confusion matrices, top confused pairs, reviewing highest-loss examples, tagging error buckets and prioritising fixes by impact."
sources:
  - https://scikit-learn.org/stable/modules/model_evaluation.html#confusion-matrix
  - https://developers.google.com/machine-learning/guides/rules-of-ml
  - https://www.deeplearning.ai/the-batch/how-to-do-error-analysis/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Confusion analysis and worst-error review

**Goal:** know *why* the model is wrong, grouped into causes you can fix, ranked by how many errors each cause explains.

## Confusion matrix done right
```python
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
ConfusionMatrixDisplay.from_predictions(y_val, y_pred, normalize="true", xticks_rotation=90)
cm = confusion_matrix(y_val, y_pred)
np.fill_diagonal(cm, 0)
pairs = sorted(((cm[i, j], labels[i], labels[j]) for i in range(len(labels)) for j in range(len(labels))), reverse=True)[:10]
```
- `normalize="true"` (rows) shows per-class recall and where each class leaks to; raw counts show where most errors are in absolute terms. Look at both.
- Top confused pairs often reveal label-definition overlap (two classes humans also confuse) rather than model weakness.

## Review the worst errors
Sort validation examples by loss (or by confidence on wrong predictions) and read 50-100 of them with the input, label and prediction side by side. Confident errors are the most informative: they're usually label errors, leakage-like shortcuts, or data the model has never seen.

## Bucket and count
Tag each reviewed error with one or more causes in a sheet:
| Bucket | Count (of 100) | Fix |
|---|---|---|
| Label wrong | 18 | relabel, guideline update |
| Blurry/low-res image | 15 | augmentation, input quality check |
| Rare subclass X | 12 | collect more X |
| Ambiguous by definition | 9 | merge classes or accept |
Prioritise by (bucket share of errors) x (feasibility). A bucket at 5% of errors caps the possible improvement at 5%.

## Repeat on slices and over time
Do the same on the worst slices from sliced evaluation and after each model change - the bucket mix shifts as you fix things.

## Gotchas
- Review on validation data, not test; once you tune against test errors the test set is spent.
- Keep a second reviewer for a sample of buckets; one person's categories drift.
- Don't fix by adding rules for individual errors; fix the cause (data, labels, features).

## Verify
- [ ] Error buckets with counts recorded for the current model.
- [ ] Next actions chosen by bucket size and feasibility.
- [ ] Re-analysis after the fix shows the targeted bucket shrank.
