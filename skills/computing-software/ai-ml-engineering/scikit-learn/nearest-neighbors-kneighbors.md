---
id: computing-software.ai-ml-engineering.scikit-learn.nearest-neighbors-kneighbors
name: nearest-neighbors-kneighbors
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, kneighborsclassifier, kneighborsregressor, nearest-neighbors, distance-metrics, ball-tree, kd-tree]
level: practitioner
status: verified
description: "Use k-nearest neighbors well: scaling, choosing k and weights, metric choice, algorithm (brute/kd_tree/ball_tree) and leaf_size, curse of dimensionality and fast ANN alternatives."
sources:
  - https://scikit-learn.org/stable/modules/neighbors.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Nearest neighbors (KNeighbors)

## Baseline recipe
```python
from sklearn.neighbors import KNeighborsClassifier
pipe = make_pipeline(StandardScaler(), KNeighborsClassifier())
grid = {"kneighborsclassifier__n_neighbors": [3, 5, 11, 21, 51],
        "kneighborsclassifier__weights": ["uniform", "distance"],
        "kneighborsclassifier__p": [1, 2]}
GridSearchCV(pipe, grid, cv=5, n_jobs=-1).fit(X, y)
```
- Scale features; distances are meaningless otherwise. The grid above picked `n_neighbors=51`, the edge of the grid, on a toy dataset: extend the grid when the best value sits at an end.
- Odd k avoids ties in binary problems; larger k smooths (more bias). `weights="distance"` helps when density varies.

## Metric
- `minkowski` with `p=2` (Euclidean, default) or `p=1` (Manhattan, more robust in higher dims).
- `metric="cosine"` for embeddings/text (forces brute force); normalize vectors and use Euclidean for an equivalent ranking with tree support (checked: identical top-5 indices).
- Mixed types: precompute a Gower distance matrix and pass `metric="precomputed"`.

## Algorithm
- `algorithm="auto"` (resolved choice read from `_fit_method`, scikit-learn 1.9.1): `brute` for sparse input, for more than 15 features (15 gave `kd_tree`, 16 gave `brute`), for `metric="cosine"` at any dimension, and when `n_neighbors` is at least half the training rows (k=50 of 100 gave `brute`, k=40 gave `kd_tree`); `kd_tree` for low-dimensional dense data including `p=1` and `chebyshev`; `ball_tree` only when the metric is not valid for the KD tree (e.g. `haversine`).
- `leaf_size` (default 30) trades build vs query time; rarely needs tuning.
- Prediction is the expensive phase (lazy learner): O(n) per query for brute force. Memory holds the full training set.

## Curse of dimensionality
In high dimensions distances concentrate: for 500 uniform random points the ratio of smallest to largest pairwise distance was 0.001 in 2 dims, 0.14 in 10, 0.45 in 50 and 0.71 in 200 (relative spread of distances 0.48, 0.20, 0.085, 0.041), so neighbors become uninformative. Reduce dimensions (PCA, learned embeddings) first or use another model.

## Large-scale search
For millions of vectors use approximate nearest neighbor libraries (FAISS, hnswlib, Annoy) and `KNeighborsTransformer` with a precomputed sparse graph to plug into sklearn pipelines.

## Other uses
`NearestNeighbors.kneighbors()` for retrieval, `RadiusNeighborsClassifier` for outlier-aware classification, KNN imputation (`KNNImputer`).

## Verify
- [ ] Validation curve over k; prediction latency measured at expected query volume.
