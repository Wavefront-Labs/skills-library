---
id: computing-software.ai-ml-engineering.scikit-learn.support-vector-machines-svc-linearsvc
name: support-vector-machines-svc-linearsvc
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, svc, linearsvc, support-vector-machines, rbf-kernel, svm-scaling, svr]
level: practitioner
status: verified
description: "Use SVMs in scikit-learn well: SVC vs LinearSVC vs SGD, mandatory scaling, C and gamma search on log grids, probability=True cost, class_weight and scaling limits."
sources:
  - https://scikit-learn.org/stable/modules/svm.html
  - https://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Support vector machines (SVC, LinearSVC)

## Choose the implementation
| n_samples | Kernel needed | Use |
|---|---|---|
| up to a few tens of thousands | non-linear (RBF, poly) | `SVC(kernel="rbf")` (libsvm; super-linear training: 0.03, 0.15, 0.55 and 1.6 s for 2k, 5k, 10k and 20k rows of 10 easy features here; harder data is slower) |
| any, high-dimensional sparse (text) | linear | `LinearSVC` (liblinear) or `SGDClassifier(loss="hinge")` |
| large, non-linear | approximate | `Nystroem` or `RBFSampler` kernel approximation + linear model (tune `gamma`: `Nystroem(gamma=0.1, n_components=200)` + `LinearSVC` scored 0.93, `RBFSampler()` at default gamma + `SGDClassifier` only 0.54) |

## Always scale
```python
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
pipe = make_pipeline(StandardScaler(), SVC(kernel="rbf", cache_size=1000))
grid = {"svc__C": np.logspace(-2, 3, 6), "svc__gamma": np.logspace(-4, 1, 6)}
GridSearchCV(pipe, grid, cv=5, n_jobs=-1).fit(X, y)
```
- `C`: inverse regularization (larger fits training data harder). `gamma`: RBF width (larger = more local, overfits). They interact; search jointly on log scales. `gamma="scale"` is the default.
- Unscaled features make the RBF distance dominated by large-range columns: with columns scaled by 1 to 1e3, 3-fold accuracy was 0.627 unscaled and 0.929 scaled.
- The grid above on 1,500 synthetic rows picked `C=1000, gamma=0.01`: `C` sits on the upper edge of the grid, which is exactly what the Verify item below warns about, so extend the grid. Scores ranged from 0.50 to 0.93 across the 6x6 grid.

## Probabilities and thresholds
- `SVC(probability=True)` is deprecated since scikit-learn 1.9 (removal in 1.11; FutureWarning: use `CalibratedClassifierCV(SVC(), ensemble=False)`); it runs internal 5-fold Platt scaling, which is slower, and probabilities can disagree with `predict` (0.4% of rows in a test). Prefer `decision_function` for ranking/AUC and use `CalibratedClassifierCV(SVC(), ensemble=False)` when you need calibrated probabilities (it ran inside a `VotingClassifier`).
- `LinearSVC` has no `predict_proba`.

## Other knobs
- `class_weight="balanced"` for imbalance.
- `LinearSVC(dual="auto")` (the default on 1.9.1) picks primal/dual by shape; `penalty="l1"` with `dual=False` gave sparse coefficients (3 of 10 exactly zero in a test).
- Multiclass: SVC uses one-vs-one internally (`decision_function_shape="ovr"` still returns 4 columns for 4 classes; `"ovo"` returns 6), LinearSVC uses one-vs-rest (`coef_` shape `(4, 10)`).
- Regression: `SVR` / `LinearSVR` with `epsilon` tube.

## When not to bother
On tabular data gradient boosting usually wins; SVMs shine on small-to-medium datasets with meaningful distances (after good feature engineering) and on text with linear kernels.

## Verify
- [ ] Heatmap of CV score over the C x gamma grid shows the best point is not on the grid edge.
