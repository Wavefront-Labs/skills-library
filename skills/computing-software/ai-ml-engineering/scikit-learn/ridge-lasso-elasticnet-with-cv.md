---
id: computing-software.ai-ml-engineering.scikit-learn.ridge-lasso-elasticnet-with-cv
name: ridge-lasso-elasticnet-with-cv
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, elasticnet, lassocv, ridgecv, regularization, linear-models]
level: practitioner
status: verified
description: "Fit Ridge, Lasso and ElasticNet in scikit-learn with RidgeCV, LassoCV and ElasticNetCV: scaling, alpha grids, l1_ratio, collinearity and reading the regularisation path."
sources:
  - https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression-and-classification
  - https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNetCV.html
  - https://scikit-learn.org/stable/auto_examples/linear_model/plot_lasso_model_selection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ridge / Lasso / ElasticNet with CV

## Which penalty
| Model | Penalty | Behaviour |
|---|---|---|
| `Ridge` | L2 | shrinks all coefficients, keeps all features; best with many correlated useful features |
| `Lasso` | L1 | sets many coefficients to exactly 0 (selection); unstable among correlated features (picks one arbitrarily) |
| `ElasticNet` | L1 + L2 (`l1_ratio`) | sparse but keeps groups of correlated features together |

## Always scale first
Penalties treat all coefficients equally, so feature units decide who gets shrunk. Put a scaler in a Pipeline so CV refits it per fold:
```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV, LassoCV, ElasticNetCV
import numpy as np
ridge = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 50)))     # efficient LOO by default
lasso = make_pipeline(StandardScaler(), LassoCV(alphas=100, cv=5, n_jobs=-1, random_state=0))   # n_alphas was removed (TypeError); alphas=int since 1.7
enet = make_pipeline(StandardScaler(), ElasticNetCV(l1_ratio=[.1, .5, .7, .9, .95, .99, 1], cv=5, n_jobs=-1))
enet.fit(X, y)
m = enet[-1]; print(m.alpha_, m.l1_ratio_, (m.coef_ != 0).sum())
```
- `RidgeCV` with the default `cv=None` uses efficient leave-one-out (GCV); passing `cv=5` ran and uses ordinary CV (use a splitter for grouped/time data).
- `LassoCV`/`ElasticNetCV` compute the full path with warm starts: much faster than GridSearchCV over alpha.
- Put most `l1_ratio` values near 1; the path is more sensitive there.
- For grouped or time-ordered data pass `cv=GroupKFold(...)` / `TimeSeriesSplit(...)`. `TimeSeriesSplit(3)` ran. `LassoCV(cv=GroupKFold(3)).fit(X, y, groups=g)` raises `ValueError: Passing extra keyword arguments to LassoCV.fit is only supported if enable_metadata_routing=True`; with `sklearn.set_config(enable_metadata_routing=True)` it ran.

## Gotchas
- sklearn's `alpha` is the overall strength; `C` in LogisticRegression/SVM is its inverse.
- Lasso convergence warnings ("Objective did not converge"): scale features, increase `max_iter`, or loosen `tol`. (A test with columns scaled by 1 to 1e5 and `alpha=0.01` did not warn, so unscaled data is a common but not guaranteed cause.)
- Sparse inputs: don't center (`StandardScaler(with_mean=False)`, or `MaxAbsScaler`; both ran); `StandardScaler()` on sparse raises `Cannot center sparse matrices: pass with_mean=False instead`.
- Coefficients after scaling are in standard-deviation units; to report in original units divide by the scaler's `scale_`.
- Lasso-selected features vary across bootstrap samples when features are correlated; check stability before calling them "the important ones". In a test with three near-duplicate predictors, 30 bootstrap `LassoCV` fits kept them in 73%, 90% and 100% of fits (2.6 of 3 on average), while `ElasticNetCV(l1_ratio=[.2,.5])` kept all three every time.
- Classification analogues: `LogisticRegressionCV(solver="saga", l1_ratios=[...])` (the `penalty="elasticnet"` argument still ran on 1.9.1 but warns that `penalty` is deprecated since 1.8), `RidgeClassifierCV` (ran).

## Inspect the path
```python
from sklearn.linear_model import lasso_path
alphas, coefs, _ = lasso_path(StandardScaler().fit_transform(X), y)
```
`lasso_path` returned `alphas` of shape (100,) and `coefs` of shape (n_features, 100). Plot `coefs.T` vs `log(alphas)` to see entry order and stability; plot `m.mse_path_.mean(axis=-1)` vs alphas to see how flat the CV curve is (consider the 1-SE rule for a sparser model).

## Verify
Compare test RMSE against plain `LinearRegression` and a `DummyRegressor`; regularisation should help most when p is large relative to n or features are collinear.
