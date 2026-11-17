---
id: computing-software.ai-ml-engineering.scikit-learn.dbscan-and-hdbscan-density-clustering
name: dbscan-and-hdbscan-density-clustering
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, dbscan, hdbscan, density-clustering, noise-points, eps-selection]
level: practitioner
status: gated
description: "Cluster by density with DBSCAN and HDBSCAN in scikit-learn: pick eps with a k-distance plot, min_samples, noise label -1, metrics, and scaling to large datasets."
sources:
  - https://scikit-learn.org/stable/modules/clustering.html#dbscan
  - https://scikit-learn.org/stable/modules/clustering.html#hdbscan
  - https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DBSCAN / HDBSCAN density clustering

Density clustering finds arbitrarily shaped clusters, doesn't need k, and labels sparse points as noise (`-1`). Good for spatial data, anomaly-adjacent tasks and embedding clusters.

## DBSCAN
```python
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
Xs = StandardScaler().fit_transform(X)
k = 10                                              # = min_samples
d, _ = NearestNeighbors(n_neighbors=k).fit(Xs).kneighbors(Xs)
plt.plot(np.sort(d[:, -1]))                         # k-distance plot: eps at the knee
db = DBSCAN(eps=0.5, min_samples=k, n_jobs=-1).fit(Xs)
labels = db.labels_; print(set(labels), (labels == -1).mean())
```
- `min_samples`: a common heuristic is 2 x n_features with a floor around 5 (rule of thumb from the DBSCAN literature, not checked here; gated: unconfirmed, source is paywalled or blocked); larger = more noise, fewer small clusters.
- `eps`: neighbourhood radius; the knee of the sorted k-distance curve. Too small: everything noise. Too large: one giant cluster.
- One `eps` for all clusters: fails when clusters have different densities. That is the reason to use HDBSCAN.
- Geographic coordinates: `metric="haversine"` on radians, eps in radians (km / 6371).

## HDBSCAN (added in scikit-learn 1.3 per its release notes: `sklearn.cluster.HDBSCAN`)
```python
from sklearn.cluster import HDBSCAN
hdb = HDBSCAN(min_cluster_size=25, min_samples=10).fit(Xs)
labels, strength = hdb.labels_, hdb.probabilities_
```
- `min_cluster_size`: smallest group you care about; the main knob.
- `min_samples`: how conservative (higher = more points become noise). Defaults to `min_cluster_size`.
- `cluster_selection_epsilon` merges clusters closer than a distance; `cluster_selection_method="leaf"` gives finer, more homogeneous clusters than default `"eom"`.
- `probabilities_` gives membership strength; the standalone `hdbscan` package adds `outlier_scores_`, soft clustering and `approximate_predict` for new points (not installed here; gated: unconfirmed, source is paywalled or blocked). `sklearn.cluster.HDBSCAN` itself has no `outlier_scores_` and no `predict` (tested).

## Practical notes
- Neither has `predict` for new data in sklearn: refit, or assign new points to the cluster of their nearest core sample (DBSCAN: `db.core_sample_indices_`).
- High dimensions: distances concentrate and density loses meaning. Reduce first (PCA to ~10-50 dims, or UMAP for embeddings, then HDBSCAN: the BERTopic recipe).
- Memory: DBSCAN with large eps builds big neighbourhoods (O(n^2) worst case). Use a smaller eps, precomputed sparse radius graph, or HDBSCAN.
- Evaluate: silhouette is biased toward convex clusters; exclude noise points when computing it, and report noise fraction.

## Verify
Plot a 2D projection coloured by label with noise in grey; check noise fraction is plausible (a few %, not 60%), and cluster sizes are not one giant plus crumbs.
