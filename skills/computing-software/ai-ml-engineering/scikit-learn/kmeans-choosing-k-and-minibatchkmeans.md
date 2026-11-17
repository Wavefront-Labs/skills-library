---
id: computing-software.ai-ml-engineering.scikit-learn.kmeans-choosing-k-and-minibatchkmeans
name: kmeans-choosing-k-and-minibatchkmeans
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, kmeans, silhouette-score, minibatchkmeans, elbow-method, clustering]
level: practitioner
status: verified
description: "Run KMeans in scikit-learn properly: scaling, n_init, choosing k with silhouette, elbow and stability, MiniBatchKMeans for large data, and when k-means is the wrong model."
sources:
  - https://scikit-learn.org/stable/modules/clustering.html#k-means
  - https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MiniBatchKMeans.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KMeans: choosing k and MiniBatchKMeans

## Fit
```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
Xs = StandardScaler().fit_transform(X)            # k-means uses Euclidean distance: scale matters
km = KMeans(n_clusters=5, n_init=10, random_state=0).fit(Xs)
labels, centers = km.labels_, km.cluster_centers_
```
- `n_init`: number of random restarts (k-means++ init); recent versions default to `"auto"` (1 run with k-means++). Use 10+ when results matter; pick the lowest inertia.
- Categorical/one-hot features distort distances; consider k-prototypes or embedding first.

## Choosing k
```python
for k in range(2, 11):
    km = KMeans(k, n_init=10, random_state=0).fit(Xs)
    print(k, km.inertia_, silhouette_score(Xs, km.labels_, sample_size=10_000, random_state=0),
          davies_bouldin_score(Xs, km.labels_))
```
- **Elbow**: inertia always decreases with k; look for the bend. Often ambiguous.
- **Silhouette** (-1..1, higher better): mean of (b - a) / max(a, b). Check the per-sample silhouette plot too: clusters with many negative values are poorly separated. `sample_size` keeps it O(n) affordable.
- **Davies-Bouldin** (lower better), **Calinski-Harabasz** (higher better) as cross-checks.
- **Stability**: refit on bootstrap samples and compare labelings with `adjusted_rand_score`; real structure is stable.
- **Usefulness**: in the end k is a business choice (segments someone can act on); metrics narrow the range.

## MiniBatchKMeans for big data
```python
from sklearn.cluster import MiniBatchKMeans
mbk = MiniBatchKMeans(n_clusters=50, batch_size=4096, n_init=3, random_state=0).fit(Xs)
# or streaming: for chunk in chunks: mbk.partial_fit(chunk)
```
Much faster for millions of rows; inertia slightly worse than full KMeans. `batch_size` defaults to 1024; the docstring suggests `batch_size > 256 * number_of_cores` to use all cores. On five blobs (2000 points) KMeans inertia was 3534.5 and MiniBatchKMeans 3535.9 (tested).

## When k-means is wrong
It assumes roughly spherical, similar-size clusters and assigns every point. Fails on elongated or nested shapes, very different densities and outliers. Alternatives: `GaussianMixture` (elliptical, soft assignments, choose components by BIC), DBSCAN/HDBSCAN (arbitrary shapes, noise), `AgglomerativeClustering` (hierarchies).

## Using clusters downstream
- Cluster IDs as a feature: fit k-means inside the pipeline/CV, not on all data first.
- `km.transform(X)` gives distances to each center: often a better feature than the label.
- Profile clusters by per-feature means in original units (inverse-transform centers).

## Verify
Labels from different seeds should agree (ARI > 0.9) if the clustering is real; visualise with PCA 2D colored by label as a sanity check, not as proof.
