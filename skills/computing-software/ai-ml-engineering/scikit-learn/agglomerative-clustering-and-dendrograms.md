---
id: computing-software.ai-ml-engineering.scikit-learn.agglomerative-clustering-and-dendrograms
name: agglomerative-clustering-and-dendrograms
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, agglomerative-clustering, hierarchical-clustering, dendrogram, linkage, ward, connectivity]
level: practitioner
status: verified
description: "Run hierarchical clustering with scikit-learn AgglomerativeClustering and SciPy linkage: ward/average/complete/single, distance thresholds, dendrograms and connectivity."
sources:
  - https://scikit-learn.org/stable/modules/clustering.html#hierarchical-clustering
  - https://scikit-learn.org/stable/auto_examples/cluster/plot_agglomerative_dendrogram.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Agglomerative clustering and dendrograms

Bottom-up: every point starts as a cluster; the closest pair merges repeatedly. No need to fix k in advance if you cut by distance.

## scikit-learn
```python
from sklearn.cluster import AgglomerativeClustering
X = StandardScaler().fit_transform(X_raw)
model = AgglomerativeClustering(n_clusters=None, distance_threshold=5.0, linkage="ward",
                                compute_distances=True).fit(X)
labels, n = model.labels_, model.n_clusters_
```
- Either `n_clusters=k` or `distance_threshold=t` (with `n_clusters=None`).
- `compute_distances=True` stores merge distances needed to plot a dendrogram.
- There is no `predict` for new points; assign new data with a classifier (e.g. KNN) trained on the labels, or use cluster centroids.

## Linkage choice
| Linkage | Merges by | Behaviour |
|---|---|---|
| `ward` | minimum increase in within-cluster variance | compact, similar-size clusters; Euclidean only; best default |
| `average` | mean pairwise distance | any metric (`metric="cosine"`), moderate |
| `complete` | max pairwise distance | compact, sensitive to outliers |
| `single` | min pairwise distance | finds elongated shapes, prone to chaining one giant cluster |

## Dendrogram with SciPy
```python
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
Z = linkage(X, method="ward")
dendrogram(Z, truncate_mode="lastp", p=30, leaf_rotation=90)
labels = fcluster(Z, t=5.0, criterion="distance")     # or criterion="maxclust", t=k
```
Pick the cut where vertical gaps between merges are largest. Cophenetic correlation (`scipy.cluster.hierarchy.cophenet(Z, pdist(X))`) measures how faithfully the tree preserves distances.

## Scale
Memory and time grow quadratically with n (pairwise distances), so measure on your data before going past tens of thousands of points. For larger data, cluster a sample or run MiniBatchKMeans to a few thousand centroids, then agglomerate the centroids.

## Connectivity constraints
```python
from sklearn.neighbors import kneighbors_graph
conn = kneighbors_graph(X, n_neighbors=10, include_self=False)
AgglomerativeClustering(n_clusters=8, connectivity=conn, linkage="ward")
```
Only neighbours may merge: gives spatially contiguous clusters (image segmentation, geography) and speeds up computation.

## Evaluate
Silhouette score across candidate cuts, cluster sizes, and domain review of members; compare with KMeans/HDBSCAN on the same features.
