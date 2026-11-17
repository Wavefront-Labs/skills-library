---
id: computing-software.ai-ml-engineering.scikit-learn.predefinedsplit-and-custom-cv-iterables
name: predefinedsplit-and-custom-cv-iterables
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, predefinedsplit, custom-cv, cross-validation, gridsearchcv, group-kfold, validation-split]
level: practitioner
status: verified
description: "Use a fixed validation set or custom fold logic in scikit-learn search: PredefinedSplit, explicit (train, test) index iterables, group and time constraints, and refit."
sources:
  - https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.PredefinedSplit.html
  - https://scikit-learn.org/stable/modules/cross_validation.html#predefined-fold-splits-validation-sets
  - https://scikit-learn.org/stable/glossary.html#term-cv
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PredefinedSplit and custom CV iterables

## Fixed validation set (single split)
When you must tune on an official validation set (or CV is too expensive), concatenate train and validation and mark rows:
```python
from sklearn.model_selection import PredefinedSplit, GridSearchCV
X = np.vstack([X_train, X_val]); y = np.concatenate([y_train, y_val])
test_fold = np.r_[np.full(len(X_train), -1), np.zeros(len(X_val), dtype=int)]  # -1 = never in test
cv = PredefinedSplit(test_fold)
search = GridSearchCV(pipe, grid, cv=cv, scoring="roc_auc", refit=True).fit(X, y)
```
- `refit=True` retrains the best model on **train + validation** combined (checked: the refit coefficients equal a pipeline fit on the concatenated data; `PredefinedSplit` with one `0` fold gives `get_n_splits() == 1`, sizes 200/100, no overlap). If you need the model trained only on train (e.g. to compare with a published baseline), set `refit=False` and fit yourself.
- Several labelled folds: use values 0..k-1 in `test_fold` (with `-1` on the first 100 rows and folds 0 and 1 on the next two blocks, `PredefinedSplit` gave 2 splits of 200 train / 100 test). With `refit=False`, `best_estimator_` does not exist (only `best_params_`).

## Any custom scheme: an iterable of index pairs
`cv` accepts any iterable of `(train_idx, test_idx)` arrays:
```python
splits = [(np.where(df.year <= y)[0], np.where(df.year == y + 1)[0]) for y in range(2019, 2024)]
cross_validate(pipe, X, y, cv=splits, scoring="neg_mean_absolute_error")
```
- Prefer a **list**. A generator also worked on scikit-learn 1.9.1 (`GridSearchCV(..., cv=generator)` gave scores identical to the list, because `check_cv` wraps the iterable into a list once), but a list is safe for your own loops, `cross_validate` calls and older code.
- Index positions, not DataFrame labels (`np.where` or `.to_numpy()`); passing `DataFrame.index` labels from a frame indexed 1000..1349 failed with `IndexError: index 1000 is out of bounds for axis 0 with size 350`.

## Built-in splitters to check first
| Need | Splitter |
|---|---|
| Groups must not span folds | `GroupKFold`, `StratifiedGroupKFold`, `LeaveOneGroupOut` |
| Temporal order | `TimeSeriesSplit(n_splits, gap=..., test_size=...)` |
| Repeated random | `RepeatedStratifiedKFold`, `ShuffleSplit` |
| Pass groups through search | `search.fit(X, y, groups=g)` |

## Custom splitter class
For reuse, implement `split(X, y=None, groups=None)` yielding index pairs and `get_n_splits(...)`; then it works everywhere `cv=` is accepted.

## Verify
```python
for tr, te in cv.split(X, y): print(len(tr), len(te), np.intersect1d(tr, te).size)
```
No overlap, expected sizes, and for groups `set(g[tr]) & set(g[te]) == set()`.
