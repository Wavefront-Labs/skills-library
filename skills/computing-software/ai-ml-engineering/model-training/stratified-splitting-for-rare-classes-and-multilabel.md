---
id: computing-software.ai-ml-engineering.model-training.stratified-splitting-for-rare-classes-and-multilabel
name: stratified-splitting-for-rare-classes-and-multilabel
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, data-splits, stratified-split, stratifiedkfold, stratifiedgroupkfold, multilabel-stratification, rare-classes]
level: practitioner
status: verified
description: "Split data so rare classes, multilabel combinations and binned regression targets appear in every fold: stratify, StratifiedGroupKFold and iterative stratification."
sources:
  - https://scikit-learn.org/stable/modules/cross_validation.html#stratification
  - https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedGroupKFold.html
  - https://github.com/trent-b/iterative-stratification
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stratified splitting for rare classes and multilabel data

**Goal:** every split has enough positives of every class to measure performance, without breaking group or time constraints.

## Single-label classification
```python
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
```
- A class with fewer members than `n_splits` raises a warning ("The least populated class in y has only 3 members, which is less than n_splits=5") and some folds get none (tested: 3 positives over 5 folds gave counts [0, 0, 1, 1, 1]). `train_test_split(stratify=y)` with a class of one member raises `ValueError: ... The minimum number of groups for any class cannot be less than 2`. Merge ultra-rare classes into "other" for splitting, or lower `n_splits`, or use `RepeatedStratifiedKFold` for more stable estimates.
- With 50 positives and a 20% test split you evaluate on 10 positives: the metric's confidence interval is enormous. Report it (bootstrap) or use CV over the whole set.

## Groups and classes together
Entities (users, patients) must not span splits, but you still want class balance:
```python
cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=0)
for tr, te in cv.split(X, y, groups=user_id): ...
```
Balance is approximate when groups are large or classes are tied to groups; check per-fold class counts (tested: 20 groups of 5 rows, one positive per group, gave 4 positives per fold and no group in both train and test).

## Multilabel
`StratifiedKFold` cannot stratify multilabel targets: with an indicator matrix it raises `ValueError: Supported target types are: ('binary', 'multiclass'). Got 'multilabel-indicator' instead` (tested on scikit-learn 1.9.1). Use iterative stratification (Sechidis et al., 2011):
```python
from iterstrat.ml_stratifiers import MultilabelStratifiedKFold
mskf = MultilabelStratifiedKFold(n_splits=5, shuffle=True, random_state=0)
for tr, te in mskf.split(X, Y): ...      # Y is the binary indicator matrix
```
It prioritises the rarest labels first so each fold gets its share (tested with `iterative-stratification`: label counts 10, 6 and 5 were spread 2/2/1/1/1-2 across 5 folds; install name `iterative-stratification`).

## Regression
Stratify on a binned target to keep the tail in every fold (ran; the held-out top-decile share was 0.10):
```python
bins = pd.qcut(y, q=10, labels=False, duplicates="drop")
train_test_split(X, y, stratify=bins, test_size=0.2, random_state=0)
```

## When not to stratify
Temporal data: future must stay in test; use time-based splits and accept class drift as part of the evaluation.

## Verify
- [ ] Per-split class (or label) counts printed and every class present in every fold.
- [ ] Group membership disjoint across splits where required.
- [ ] Test-set positive count large enough for the reported precision/recall to mean something.
