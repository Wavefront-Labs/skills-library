---
id: computing-software.ai-ml-engineering.scikit-learn.importance-with-correlated-features
name: importance-with-correlated-features
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, correlated-features-importance, permutation-importance, feature-clustering, multicollinearity, spearman]
level: practitioner
status: gated
description: "Get reliable feature importance when features are correlated: why permutation and impurity importances mislead, and clustering features by Spearman correlation first."
sources:
  - https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance_multicollinear.html
  - https://scikit-learn.org/stable/modules/permutation_importance.html
  - https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Importance with correlated features

## The problem
- **Permutation importance**: shuffling one of two correlated features barely hurts, because the model reads the same signal from the other. Both look unimportant even if the pair is crucial.
- **Impurity (MDI) importance**: splits importance arbitrarily between correlated features and is biased toward high-cardinality features (gated: unconfirmed, source is paywalled or blocked).
- **Coefficients**: unstable with collinearity (large opposite-signed coefficients).

## Clustered permutation importance
1. Compute Spearman rank correlation and cluster features hierarchically.
2. Keep one representative per cluster (or permute the whole cluster jointly).
```python
from scipy.stats import spearmanr
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform
corr = spearmanr(X_train).correlation
corr = (corr + corr.T) / 2; np.fill_diagonal(corr, 1)
link = hierarchy.ward(squareform(1 - np.abs(corr)))
cluster_ids = hierarchy.fcluster(link, t=1.0, criterion="distance")
keep = [np.where(cluster_ids == c)[0][0] for c in np.unique(cluster_ids)]
```
3. Refit on `X[:, keep]` and compute permutation importance on held-out data:
```python
from sklearn.inspection import permutation_importance
r = permutation_importance(model, X_val[:, keep], y_val, n_repeats=20, random_state=0, scoring="roc_auc")
```
The importance of a representative now stands for the whole cluster. The clustering code ran (Spearman correlation, Ward linkage, `fcluster`) on 10 features with 4 redundant ones and produced 4 clusters; `squareform` raises "Distance matrix 'X' must be symmetric" on an unsymmetrised matrix, which is why the `(corr + corr.T) / 2` line is needed (tested). Plot the dendrogram so readers see which features each one represents.

## Group permutation without refitting
Permute all columns of a cluster with the same row permutation and measure the drop; this keeps within-cluster correlation intact and measures the group's joint importance. Implement with a loop over clusters (scikit-learn's function permutes single columns).

## Choosing the threshold
`t` in `fcluster` sets how correlated features must be to group. Try several; report importance at a threshold where clusters make domain sense.

## Other tools
- SHAP values split credit among correlated features too (interventional SHAP); sum SHAP values within a cluster for group importance.
- Drop-column importance (refit without each feature or group) is the most direct but expensive.

## Verify
Model score after dropping to representatives should be close to the full model; if it drops a lot, the threshold merged features that carry distinct information.
