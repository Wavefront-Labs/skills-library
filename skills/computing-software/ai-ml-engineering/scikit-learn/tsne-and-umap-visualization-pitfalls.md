---
id: computing-software.ai-ml-engineering.scikit-learn.tsne-and-umap-visualization-pitfalls
name: tsne-and-umap-visualization-pitfalls
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, tsne, umap, manifold-learning, embedding-visualization, perplexity]
level: practitioner
status: verified
description: "Visualise high-dimensional data with t-SNE and UMAP without misreading them: perplexity and n_neighbors, PCA initialisation, and what cluster sizes and distances do not mean."
sources:
  - https://scikit-learn.org/stable/modules/manifold.html#t-distributed-stochastic-neighbor-embedding-t-sne
  - https://distill.pub/2016/misread-tsne/
  - https://umap-learn.readthedocs.io/en/latest/parameters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# t-SNE / UMAP visualization pitfalls

## t-SNE
```python
from sklearn.manifold import TSNE
X50 = PCA(n_components=50, random_state=0).fit_transform(StandardScaler().fit_transform(X))   # denoise + speed
Z = TSNE(n_components=2, perplexity=30, init="pca", learning_rate="auto", random_state=0).fit_transform(X50)
```
- `perplexity` ~ effective number of neighbours (5-50; must be < n_samples: `ValueError: perplexity (2000) must be less than n_samples (100)`). Try several; structure that appears only at one setting is suspect. On the 1,797-image digits set trustworthiness was 0.9847, 0.9886 and 0.9829 for perplexity 5, 30 and 100.
- `init="pca"` (the default on 1.9.1, with `learning_rate="auto"`) preserves more global layout and is more reproducible than random: two `init="random"` runs with different seeds correlated -0.58 on the first axis.
- No `transform` for new points (`hasattr(TSNE, "transform")` is False): t-SNE is for visualisation only, never as model features.
- Cost grows with the number of points (the 1,797-point digits set was fine; large data was not tested).

## UMAP (umap-learn)
```python
import umap
Z = umap.UMAP(n_neighbors=15, min_dist=0.1, metric="cosine", random_state=42).fit_transform(X)
```
- `n_neighbors`: local (5) vs global (50-200) structure. `min_dist`: how tightly points pack (0.0 for clustering downstream, 0.1-0.5 for viewing).
- Has `transform` for new points (ran: 10 new rows mapped); `random_state=42` made two runs identical (umap-learn 0.5.12, Python 3.12; 1,797 x 64 digits took about 3 s with or without a seed, plus numba compilation on the first call).
- `metric="cosine"` for text/image embeddings.

## What the plots do not tell you
- **Cluster sizes mean nothing**: t-SNE expands dense clusters and contracts sparse ones.
- **Distances between clusters mean little**: far-apart blobs aren't necessarily more different than near ones (UMAP preserves global structure somewhat better, still not reliably).
- **Random noise can look clustered** at low perplexity.
- **Shapes of clusters** are artefacts of the optimisation.
- Different runs/seeds rotate, flip and rearrange clusters.

## Good practice
- Colour by known labels or metadata to check hypotheses rather than discovering "clusters" from the picture.
- Confirm any structure with a method that works in the original space (clustering metrics, nearest-neighbour label agreement, a classifier).
- Show several parameter settings side by side in reports.
- Don't cluster on t-SNE coordinates; UMAP-then-HDBSCAN is acceptable with `min_dist=0` and more components (5-10), and should be validated. On digits with `sklearn.cluster.HDBSCAN(min_cluster_size=20)`, adjusted Rand index against the true digits was 0.889 (2-d, `min_dist=0.1`), 0.903 (2-d, `min_dist=0`), 0.914 (8-d, `min_dist=0`) and 0.811 on t-SNE coordinates (10 clusters found, 13-14 for UMAP), so UMAP did a little better here, not dramatically.
- Large datasets: subsample for plotting, but keep rare classes.

## Verify
Trustworthiness score (`sklearn.manifold.trustworthiness(X, Z, n_neighbors=10)`, closer to 1 is better) to compare settings (digits: t-SNE 0.9886, UMAP cosine 0.9883); kNN label accuracy in Z vs in X to check how much neighbourhood information survived (5-fold, k=5: original 0.963, t-SNE 0.955, UMAP 0.982).
