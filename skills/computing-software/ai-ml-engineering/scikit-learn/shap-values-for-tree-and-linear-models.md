---
id: computing-software.ai-ml-engineering.scikit-learn.shap-values-for-tree-and-linear-models
name: shap-values-for-tree-and-linear-models
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, shap, treeexplainer, feature-attribution, model-explainability, shap-values]
level: practitioner
status: verified
description: "Explain scikit-learn, XGBoost and LightGBM models with SHAP: TreeExplainer vs LinearExplainer, background data, global and local plots, and interpretation pitfalls."
sources:
  - https://shap.readthedocs.io/en/latest/
  - https://shap.readthedocs.io/en/latest/example_notebooks/tabular_examples/tree_based_models/Front%20page%20example%20(XGBoost).html
  - https://arxiv.org/abs/1705.07874
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SHAP values for tree and linear models

SHAP assigns each feature a contribution such that `base_value + sum(shap_values) = model output` for every row (local accuracy). Global importance = mean |SHAP|.

## Trees (fast, exact)
```python
import shap
explainer = shap.TreeExplainer(model)                     # XGBoost, LightGBM, sklearn trees/forests (all ran)
sv = explainer(X_val)                                      # shap.Explanation
shap.plots.beeswarm(sv)                                    # global: importance + direction
shap.plots.bar(sv)                                         # mean |SHAP|
shap.plots.waterfall(sv[0])                                # one prediction
shap.plots.scatter(sv[:, "income"], color=sv)              # dependence + strongest interaction
```
- Output space (shap 0.54.1, XGBoost 3.4.1): for an XGBoost classifier `TreeExplainer` values are in log-odds (raw margin): `values.sum(1) + base_values` matched `predict(..., output_margin=True)`. `TreeExplainer(m, data=background, feature_perturbation="interventional", model_output="probability")` gave probability units and additivity against `predict_proba` held (slower). Sklearn `RandomForestClassifier` values come back with a class axis, shape `(n, n_features, 2)`; LightGBM binary gave `(n, n_features)`.
- `feature_perturbation="tree_path_dependent"` (the reported default for `TreeExplainer(model)`) uses the trees' cover statistics; `"interventional"` with a background sample (100-1000 rows) breaks feature dependence explicitly. They can differ for correlated features.

## Linear models
```python
explainer = shap.LinearExplainer(lr_pipeline[-1], shap.maskers.Independent(Xs_background))
sv = explainer(Xs_val)
```
For an independent masker, SHAP_i = coef_i x (x_i - mean(x_i)): just centered contributions, with the mean taken over the masker's background. `shap.maskers.Independent` subsamples the background to `max_samples=100` rows by default (it prints a message), so the formula matched only with `Independent(Xs, max_samples=len(Xs))` (max difference 0.0, against 0.12 with the default). `LinearExplainer(lr, X)` with a raw array behaved the same way. Pass the transformed features the linear model actually sees (after the pipeline's preprocessing) and map names via `get_feature_names_out()`.

## Model-agnostic
`shap.Explainer(model.predict_proba, masker)` picks the algorithm itself: `ExactExplainer` for 7 features, `PermutationExplainer` for 30. It is slow on large inputs; use small backgrounds (`shap.sample(X, 100)`) and subsample rows. Output has a class axis, shape `(n, n_features, 2)` for `predict_proba`.

## Pitfalls
- **Correlated features** split credit unpredictably; grouping them (sum SHAP within a group) is more honest than ranking individuals.
- **Not causal**: high SHAP means the model uses the feature, not that changing it changes the outcome.
- **One-hot features**: sum SHAP across a categorical's dummy columns to get the variable's contribution.
- **Data leakage shows up here first**: a surprisingly dominant feature (an ID, a timestamp, a post-outcome field) deserves investigation.
- **Explaining the wrong data**: compute on held-out data representative of production.
- Global mean |SHAP| ranks differ from permutation importance: SHAP measures use, permutation measures dependence of performance. Report both when they disagree.

## Verify
`np.allclose(sv.values.sum(1) + sv.base_values, model_output)` in the explainer's output space (e.g. `model.predict(X, output_margin=True)` for XGBoost). Sanity-check by adding a random noise feature: it should rank below the real signals. In a test with 100 XGBoost trees the noise column got mean |SHAP| 0.215 (5% of the total) against 0.27 to 1.14 for the real columns, i.e. small but not zero. `TreeExplainer` also accepted a `HistGradientBoostingClassifier` and its values summed to `decision_function` (checked).
