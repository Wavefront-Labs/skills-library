---
id: computing-software.ai-ml-engineering.scikit-learn.monotonic-and-interaction-constraints
name: monotonic-and-interaction-constraints
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, monotonic-constraints, interaction-constraints, histgradientboosting, model-governance]
level: practitioner
status: verified
description: "Enforce monotonic and interaction constraints in HistGradientBoosting, LightGBM and XGBoost so predictions move in the expected direction for regulated or trusted models."
sources:
  - https://scikit-learn.org/stable/modules/ensemble.html#monotonic-constraints
  - https://scikit-learn.org/stable/modules/ensemble.html#interaction-constraints
  - https://xgboost.readthedocs.io/en/stable/tutorials/monotonic.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monotonic and interaction constraints

When domain knowledge says "more income never lowers the credit score" or "price up never raises predicted demand", a constraint enforces it. Benefits: predictions explainable to regulators and users, robustness to noise and to extrapolation, sometimes better generalisation on small data.

## scikit-learn HistGradientBoosting
```python
from sklearn.ensemble import HistGradientBoostingRegressor
hgb = HistGradientBoostingRegressor(
    monotonic_cst={"income": 1, "debt_ratio": -1},          # dict by column name (DataFrame input) or list
    interaction_cst=[[2, 0], [3, 4]],                        # POSITIONS of age/income and region/product in X_df (names are rejected)
    categorical_features="from_dtype")
hgb.fit(X_df, y)
```
- `1` increasing, `-1` decreasing, `0` unconstrained. Lists must align with column order. `monotonic_cst` accepts a dict of names (since 1.2), but `interaction_cst` takes feature indices only: passing names raised `ValueError: Interaction constraints must consist of integer indices in [0, n_features - 1]` on 1.9.1. The strings `"pairwise"` and `"no_interactions"` are also accepted. A monotonic fit passed a check that raising `income` by 0.05 never lowered predictions (the unconstrained model failed it).
- Monotonic constraints are not supported on categorical features (`ValueError: Categorical features cannot have monotonic constraints.`).
- For binary classification constraints apply to the log-odds (so to probabilities too). Multiclass monotonic constraints are not supported (`ValueError: monotonic constraints are not supported for multiclass classification.`); a binary classifier's `predict_proba` was monotone in the constrained feature in a check.

## XGBoost / LightGBM
```python
xgb.XGBRegressor(monotone_constraints={"income": 1, "debt_ratio": -1},
                 interaction_constraints=[["age", "income"], ["region", "product"]], tree_method="hist")
lgb.LGBMRegressor(monotone_constraints=[1, -1, 0, 0], monotone_constraints_method="advanced")
```
Both libraries accepted these arguments (xgboost with feature names for `monotone_constraints` and `interaction_constraints`, lightgbm 4.7.0) and the constrained predictions were monotone. LightGBM's methods differ in how restrictive they are, but I did not find `"advanced"` always best: training R2 was 0.587 for `"basic"`, 0.599 for `"intermediate"` and 0.594 for `"advanced"` on one synthetic set, so compare them on validation data; `monotone_penalty` is also accepted (see the LightGBM docs for its definition; its effect was not measured here).

## Interaction constraints
Features in the same group may interact (appear on the same tree path); features in different groups can't. Use to build additive models that are easier to explain (e.g. each group's contribution can be plotted separately), or to block known-spurious interactions. In HGB, features not listed in any group are treated together as one additional group (per the docstring: `[{0, 1}]` equals `[{0, 1}, {2, 3, 4}]` with 5 features); they are not excluded (an unlisted `debt_ratio` still moved predictions by 0.109 in a check). To allow only main effects, give every feature its own group, e.g. `[[0], [1], ...]`, or use `"no_interactions"`.

## Choosing constraints
- Only constrain where the relationship is causal or mandated, not just observed in this data.
- Interactions can hide monotonicity: a feature monotonic overall may not be monotonic within every segment; the constraint enforces it everywhere.
- Expect a small accuracy drop on the training distribution; compare on validation. If it drops a lot, the assumption may be wrong or the feature leaks.

## Linear models
For linear models, monotonicity means sign constraints: `LinearRegression(positive=True)` or `Lasso(positive=True)`.

## Verify
Partial dependence and ICE plots for constrained features must be monotonic for every individual curve:
```python
from sklearn.inspection import PartialDependenceDisplay
PartialDependenceDisplay.from_estimator(hgb, X_df, ["income"], kind="individual")
```
Also check programmatically: increase the feature by a delta for all rows and assert predictions never decrease.
