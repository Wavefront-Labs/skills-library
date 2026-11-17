---
id: computing-software.ai-ml-engineering.scikit-learn.gaussian-mixture-models-bic
name: gaussian-mixture-models-bic
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, gaussian-mixture, bic, aic, soft-clustering, density-estimation, bayesiangaussianmixture]
level: practitioner
status: verified
description: "Fit Gaussian mixture models: covariance_type choice, selecting components with BIC/AIC, n_init and initialization, soft assignments, density scoring and BayesianGaussianMixture."
sources:
  - https://scikit-learn.org/stable/modules/mixture.html
  - https://scikit-learn.org/stable/auto_examples/mixture/plot_gmm_selection.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.mixture.GaussianMixture.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gaussian mixture models and BIC selection

**Use for:** soft clustering (membership probabilities), elliptical clusters of different sizes, and density estimation (anomaly scoring via low likelihood).

## Fit and select K
```python
from sklearn.mixture import GaussianMixture
Xs = StandardScaler().fit_transform(X)
results = []
for cov in ["spherical", "diag", "tied", "full"]:
    for k in range(1, 11):
        gm = GaussianMixture(k, covariance_type=cov, n_init=5, random_state=0).fit(Xs)
        results.append((gm.bic(Xs), cov, k))
best_bic, best_cov, best_k = min(results)
```
- Lower BIC is better; BIC penalizes parameters more than AIC and tends to pick fewer components.
- Parameter count grows fast with `full` covariance (k x d x (d+1)/2): in high dimensions use `diag` or reduce dimensions first.

## Use the model
```python
gm = GaussianMixture(best_k, covariance_type=best_cov, n_init=5, random_state=0).fit(Xs)
labels = gm.predict(Xs); probs = gm.predict_proba(Xs)           # soft memberships
log_density = gm.score_samples(Xs)                               # anomaly score: low = unusual
threshold = np.percentile(log_density, 1)
```

## Practical knobs
- `n_init` (a few, e.g. 5) to avoid bad local optima; `init_params` defaults to `"kmeans"` (`"k-means++"`, `"random"` and `"random_from_data"` are accepted); `max_iter` if convergence warnings appear.
- `reg_covar` (default 1e-6) prevents singular covariances when a component collapses onto few points or duplicated values; raise it if you see errors.
- Check `gm.converged_`.

## BayesianGaussianMixture
Set a generous `n_components` and a Dirichlet process prior (`weight_concentration_prior_type="dirichlet_process"`, small `weight_concentration_prior`); unused components get near-zero weights, giving an automatic K estimate (tested: `n_components=10` on 3 blobs left three weights near 0.33 and the rest near 0.002 or 0).

## Limits
Assumes roughly Gaussian clusters; use HDBSCAN for arbitrary shapes and noise. Results depend on scaling.

## Verify
- [ ] Plot BIC vs k per covariance type; inspect component weights (`gm.weights_`) for tiny components.
