---
id: computing-software.ai-ml-engineering.scikit-learn.clustering-evaluation-ari-davies-bouldin
name: clustering-evaluation-ari-davies-bouldin
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, cluster-evaluation, adjusted-rand-index, davies-bouldin, calinski-harabasz, clustering-stability]
level: practitioner
status: verified
description: "Evaluate clusterings: internal indices (silhouette, Davies-Bouldin, Calinski-Harabasz), external ARI/AMI/V-measure when labels exist, and bootstrap stability checks."
sources:
  - https://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.davies_bouldin_score.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Clustering evaluation

**There is no single right score.** Combine an internal index, stability, and whether clusters are useful to the business.

## Internal indices (no ground truth)
| Metric | Better | Notes |
|---|---|---|
| `silhouette_score(X, labels)` | higher (-1..1) | O(n^2); use `sample_size=` for large n |
| `davies_bouldin_score(X, labels)` | lower (0 best) | cheap; favors compact, separated clusters |
| `calinski_harabasz_score(X, labels)` | higher | cheap; favors convex clusters |
All three favor convex, KMeans-like clusters and penalize DBSCAN-style shapes; exclude noise points (label -1) before scoring.

## External indices (some reference labels)
- `adjusted_rand_score(true, pred)`: chance-corrected pair agreement; 0 = random, 1 = identical.
- `adjusted_mutual_info_score`: information-based, chance-corrected; better with unequal cluster sizes.
- `homogeneity_completeness_v_measure`: whether clusters are pure vs whether classes stay together.
- Labels are permutation-invariant; never use accuracy directly.

## Stability
```python
from sklearn.metrics import adjusted_rand_score
rng = np.random.default_rng(0); base = KMeans(k, n_init=10, random_state=0).fit(X)
scores = []
for _ in range(20):
    idx = rng.choice(len(X), size=int(0.8 * len(X)), replace=False)
    m = KMeans(k, n_init=10, random_state=int(rng.integers(1e9))).fit(X[idx])
    scores.append(adjusted_rand_score(base.predict(X[idx]), m.labels_))
print(np.mean(scores))     # close to 1 = stable partition
```
Repeat for candidate k; prefer k with high stability and reasonable internal scores.

## Usefulness checks
- Profile clusters (feature means/medians per cluster, sizes) and give each a human-readable description.
- Downstream validation: do clusters differ on an outcome they were not built from (churn, spend)?

## Verify
- [ ] Table of k vs silhouette/DB/CH/stability; chosen k justified in writing.
