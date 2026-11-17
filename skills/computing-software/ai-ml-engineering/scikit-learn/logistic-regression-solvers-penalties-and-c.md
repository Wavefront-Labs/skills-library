---
id: computing-software.ai-ml-engineering.scikit-learn.logistic-regression-solvers-penalties-and-c
name: logistic-regression-solvers-penalties-and-c
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, logistic-regression-solvers, logisticregression, regularization, multinomial, class-weight]
level: practitioner
status: verified
description: "Configure scikit-learn LogisticRegression: pick solver by penalty and data size, tune C, handle multiclass, convergence warnings, class_weight and coefficient reading."
sources:
  - https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
  - https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegressionCV.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LogisticRegression solvers, penalties and C

Default `LogisticRegression()` is L2-regularised with `C=1.0` and `lbfgs`. It is never plain unpenalised logistic regression unless you disable the penalty. In scikit-learn 1.8+ the `penalty` argument is deprecated (removal planned for 1.10): use `l1_ratio` (0 = L2, 1 = L1, between = elastic net) and `C=np.inf` for no penalty. The table below still uses the old `penalty` names, which work on 1.9.1 with a `FutureWarning`.

## Solver table
| Solver | Penalties | Notes |
|---|---|---|
| `lbfgs` (default) | l2, None | good default for dense, small-medium data; multinomial |
| `liblinear` | l1, l2 | small data; binary only on 1.9.1 (multiclass raises, wrap in `OneVsRestClassifier`); penalises the intercept |
| `newton-cg` | l2, None | multinomial; accurate |
| `newton-cholesky` | l2, None | fast when n_samples >> n_features (dense, few hundred features) |
| `sag` | l2, None | large n; needs scaled features |
| `saga` | l1, l2, elasticnet, None | large or sparse data, the only elasticnet option; needs scaled features |
Wrong combinations raise e.g. `ValueError: Solver lbfgs supports only 'l2' or None penalties, got l1 penalty.`; `liblinear` with elasticnet raises `Only 'saga' solver supports elasticnet penalty`. Combinations in the table were all run on 1.9.1.

## Pattern
```python
from sklearn.linear_model import LogisticRegressionCV
clf = make_pipeline(StandardScaler(),
                    LogisticRegressionCV(Cs=np.logspace(-4, 2, 20), cv=5, scoring="neg_log_loss",
                                         max_iter=2000, n_jobs=-1))
clf.fit(X, y); print(clf[-1].C_)
```
- `C` is inverse regularisation: smaller = stronger. Search on a log grid.
- Score with `neg_log_loss` or `roc_auc` when you care about probabilities, not accuracy.

## Convergence warnings
`ConvergenceWarning: lbfgs failed to converge` almost always means unscaled features. Scale first; then raise `max_iter` (1000-5000). Do not ignore it: coefficients are not at the optimum.

## Multiclass
On 1.9.1 every solver except liblinear fits a multinomial (softmax) model; `liblinear` raises `The 'liblinear' solver does not support multiclass classification`, and the `multi_class` parameter has been removed (`TypeError: unexpected keyword argument`). For one-vs-rest, wrap with `OneVsRestClassifier`.

## Imbalance
`class_weight="balanced"` reweights the loss; it shifts predicted probabilities, so calibrate or tune the decision threshold afterwards (`TunedThresholdClassifierCV`) and don't read the probabilities as base rates.

## Interpreting coefficients
- With standardised inputs, `coef_` is the change in log-odds per one-SD increase; `np.exp(coef_)` is the odds ratio.
- Regularisation biases coefficients toward 0; for inference with p-values and CIs, use statsmodels `Logit` (unpenalised), not sklearn.
- Perfect separation: unpenalised fits diverge; sklearn's default L2 keeps them finite.

## Verify
Check `n_iter_` is below `max_iter`, and compare `log_loss` on held-out data against `DummyClassifier(strategy="prior")`.
