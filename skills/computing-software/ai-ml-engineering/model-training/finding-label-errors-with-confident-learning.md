---
id: computing-software.ai-ml-engineering.model-training.finding-label-errors-with-confident-learning
name: finding-label-errors-with-confident-learning
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, error-analysis, label-noise, cleanlab, confident-learning, out-of-fold-predictions, data-quality]
level: practitioner
status: draft
description: "Find mislabeled training and test examples with confident learning: out-of-fold predicted probabilities, cleanlab find_label_issues and Datalab, review workflow and pitfalls."
sources:
  - https://arxiv.org/abs/1911.00068
  - https://arxiv.org/abs/2103.14749
  - https://docs.cleanlab.ai/stable/index.html
  - https://docs.cleanlab.ai/stable/cleanlab/filter.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Finding label errors with confident learning

**Goal:** locate likely mislabeled examples so humans can fix them - noisy labels cap model accuracy and corrupt test metrics (Northcutt et al. found errors in the test sets of many standard benchmarks).

## Out-of-fold probabilities first
Confident learning needs predicted probabilities for each example from a model that did **not** train on it:
```python
from sklearn.model_selection import cross_val_predict
pred_probs = cross_val_predict(model, X, y, cv=5, method="predict_proba")   # shape (n, n_classes)
```
For deep nets, do K-fold training or at least use a held-out-trained model's predictions. In-sample probabilities make the model "agree" with wrong labels it memorised.

## Find issues
```python
from cleanlab.filter import find_label_issues
idx = find_label_issues(labels=y, pred_probs=pred_probs, return_indices_ranked_by="self_confidence")
review = df.iloc[idx[:200]]          # most likely errors first
```
Or the broader audit:
```python
from cleanlab import Datalab
lab = Datalab(data=df, label_name="label")
lab.find_issues(pred_probs=pred_probs, features=embeddings)   # label issues + outliers + near-duplicates
lab.report()
```
Under the hood: per-class confidence thresholds (average predicted probability of each class among examples labeled with it) estimate the joint distribution of noisy vs true labels, then flag the examples most likely off-diagonal.

## Workflow
1. Review flagged examples in rank order with a domain expert; record decision (relabel / keep / ambiguous / remove).
2. Track the precision of the flags (what fraction were truly wrong) to decide how deep to go.
3. Fix labels in the source of truth, not just in a training copy.
4. Retrain and compare on a **cleaned test set** too; noisy test labels can hide real improvements.

## Pitfalls
- Systematic label errors (a whole subclass labeled wrong by a guideline) look "consistent" and may not be flagged; error analysis by slice catches those.
- Rare classes get flagged more because the model is weak on them - review, don't auto-delete.
- Auto-removing flagged examples can delete the hard, informative cases; prefer relabeling.

## Verify
- [ ] Probabilities are out-of-fold.
- [ ] Flag precision measured on a reviewed sample.
- [ ] Test-set labels audited, and metrics reported on the cleaned test set.
