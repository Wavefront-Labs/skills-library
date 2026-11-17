---
id: computing-software.ai-ml-engineering.scikit-learn.pipeline-memory-caching
name: pipeline-memory-caching
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, pipeline-memory-caching, pipeline, joblib-memory, gridsearchcv, performance]
level: practitioner
status: verified
description: "Speed up grid searches over a Pipeline by caching fitted transformers with memory=, plus the named_steps gotcha and cache invalidation."
sources:
  - https://scikit-learn.org/stable/modules/compose.html#caching-transformers-avoid-repeated-computation
  - https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html
  - https://joblib.readthedocs.io/en/stable/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline memory caching

**Goal:** stop recomputing an expensive transformer (PCA on wide data, text vectorisation, feature extraction) for every hyperparameter combination that only changes the final estimator.

## Turning it on
```python
from tempfile import mkdtemp
from shutil import rmtree
from joblib import Memory

cachedir = mkdtemp()      # any scratch folder works; the examples here used a fixed folder
pipe = Pipeline([("tfidf", TfidfVectorizer()), ("svd", TruncatedSVD(300)), ("clf", LogisticRegression())],
                memory=Memory(location=cachedir, verbose=0))
search = GridSearchCV(pipe, {"clf__C": [0.01, 0.1, 1, 10]}, cv=5, n_jobs=-1).fit(X, y)
rmtree(cachedir)
```
- Every transformer's `fit_transform` result is cached keyed by its parameters and input data. Grid points that differ only in `clf__C` reuse the cached TF-IDF and SVD for each fold: a counting transformer was fit 21 times without `memory` (4 grid points x 5 folds + 1 refit) and 6 times with it (5 folds + 1 refit), single process on 1.9.1.
- The final step is never cached.
- `memory="some/dir"` (string) also works; `joblib.Memory` gives control over verbosity and compression.

## The named_steps gotcha
With caching on, the pipeline clones each transformer before fitting. The object you passed in is **not** the fitted one:
```python
svd = TruncatedSVD(300)
pipe = Pipeline([("svd", svd), ("clf", clf)], memory=cachedir).fit(X, y)
svd.components_                    # AttributeError: not fitted
pipe.named_steps["svd"].components_  # correct
```

## When it does not help
- When the grid changes parameters of early steps, each combination is a new cache key; caching then only helps across repeated runs.
- Cheap transformers (StandardScaler) cost more to hash and pickle than to recompute. Hashing large `X` is itself not free.
- Results are pickled to disk; for huge intermediates the disk I/O can exceed recompute time. Use a fast local disk, not a network share.

## Invalidation
The key includes the transformer class, its parameters and input data, not its source code. Reproduced: after editing a custom transformer's `fit` and `transform` in its module with unchanged params, the second pipeline fit did not call the new `fit` (cache hit); only `transform` ran the new code, so the fitted state was stale. Clear the cache (`Memory.clear()` or delete the directory) after code changes, and use a temp dir per experiment.

## Verify
- [ ] Search wall time drops when only final-estimator params vary.
- [ ] Fitted attributes read via `named_steps`/`best_estimator_`, not original objects.
- [ ] Cache directory removed or isolated per experiment.
