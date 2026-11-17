---
id: computing-software.ai-ml-engineering.scikit-learn.pca-truncatedsvd-and-explained-variance
name: pca-truncatedsvd-and-explained-variance
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, pca, truncatedsvd, explained-variance, dimensionality-reduction, incrementalpca]
level: practitioner
status: verified
description: "Reduce dimensions with PCA and TruncatedSVD in scikit-learn: scaling, choosing components by explained variance, sparse inputs, whitening and using PCA inside pipelines."
sources:
  - https://scikit-learn.org/stable/modules/decomposition.html#pca
  - https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.IncrementalPCA.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PCA / TruncatedSVD and explained variance

## PCA on dense data
```python
from sklearn.decomposition import PCA
pipe = make_pipeline(StandardScaler(), PCA(n_components=0.95, svd_solver="full"))   # keep 95% variance
Z = pipe.fit_transform(X)
pca = pipe[-1]
print(pca.n_components_, pca.explained_variance_ratio_.cumsum()[:10])
```
- **Scale first** unless all features share units; otherwise the largest-variance feature dominates PC1 (multiplying one `load_digits` pixel column by 1000 made it PC1 with 99.996% of the variance; scaled, PC1 explains 12%).
- `n_components` as a float in (0,1) picks enough components for that variance fraction (40 components for 95% on scaled `load_digits`); as an int fixes the count. A float is rejected with `svd_solver="randomized"` (`n_components=0.95 must be between 1 and min(n_samples, n_features)=64 with svd_solver='randomized'`).
- Large data: `svd_solver="randomized"` (fast for few components); `IncrementalPCA(batch_size=...)` with `partial_fit` for out-of-core.

## Choosing components
- Cumulative explained variance plot: look for a plateau; 90-99% are common cut-offs.
- Scree plot elbow.
- For a downstream model, treat `n_components` as a hyperparameter and tune by CV score: variance retained is not the same as predictive information.

## TruncatedSVD for sparse matrices
```python
from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components=300, algorithm="randomized", n_iter=7, random_state=0)
Z = svd.fit_transform(tfidf_matrix)          # works on scipy.sparse without densifying; returns a dense ndarray (2236 x 300 on a 4-class 20 newsgroups subset, 37.7% variance explained)
```
Plain PCA centers the data, which would densify a sparse matrix; TruncatedSVD doesn't center. On scikit-learn 1.9.1 `PCA` does accept `scipy.sparse` input, but only with `svd_solver` `"arpack"` or `"covariance_eigh"` (`auto` picked a working one; `"full"` and `"randomized"` raise `PCA only support sparse inputs with the "arpack" and "covariance_eigh" solvers`) and gave the same variance ratios as dense PCA (0.5450 for 5 components on digits); `covariance_eigh` was added in 1.5. On TF-IDF this is LSA. Normalise rows afterwards (`Normalizer()`) for cosine-based uses.

## Options and interpretation
- `whiten=True` scales components to unit variance (useful before some models); it amplifies noise in small components.
- `pca.components_` are loadings (rows = components, columns = original features); examine the top-weighted features per component. Signs are arbitrary (fits with different solvers returned the same component up to the sign flip: `allclose(a, b)` was True in the run, False for `-b`, so not guaranteed across versions or solvers).
- `pca.inverse_transform(Z)` reconstructs; reconstruction error per row is a simple anomaly score.

## Gotchas
- Fit PCA inside the CV pipeline. Fitting on all data before splitting leaks test-set structure.
- PCA is linear; it won't unfold curved manifolds. For visualisation of nonlinear structure use t-SNE/UMAP (but not as model features without care).
- Tree models rarely benefit from PCA; it mixes features and can hurt interpretability (RandomForest on `load_digits`, 3-fold accuracy 0.942 raw vs 0.918 after scaled PCA at 95%).
- Many near-duplicate features (collinearity): PCA helps linear models; so does ridge.

## Verify
`pca.explained_variance_ratio_.sum()` matches what you intended; downstream CV score with PCA vs without; reconstruction error on held-out data similar to training.
