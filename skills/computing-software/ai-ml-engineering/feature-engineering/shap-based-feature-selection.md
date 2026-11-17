---
id: computing-software.ai-ml-engineering.feature-engineering.shap-based-feature-selection
name: shap-based-feature-selection
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, shap-feature-selection, shap, feature-selection, treeshap, shap-select, borutashap]
level: practitioner
status: draft
description: "Select features using SHAP values: global mean |SHAP| rankings, recursive elimination by SHAP, BorutaSHAP and shap-select, with held-out evaluation and pitfalls."
sources:
  - https://shap.readthedocs.io/en/latest/
  - https://github.com/Ekeany/Boruta-Shap
  - https://github.com/ing-bank/probatus
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SHAP-based feature selection

SHAP values attribute each prediction to features additively. Mean absolute SHAP per feature is a global importance that accounts for interactions and is consistent (Lundberg and Lee), making it a better ranking than impurity importance.

## Ranking
```python
import shap
model = lgb.LGBMClassifier(n_estimators=500, learning_rate=0.05).fit(X_tr, y_tr)
explainer = shap.TreeExplainer(model)
sv = explainer.shap_values(X_va)                 # compute on validation data
sv = sv[1] if isinstance(sv, list) else sv       # older versions return per-class lists
global_imp = pd.Series(np.abs(sv).mean(0), index=X_va.columns).sort_values(ascending=False)
shap.summary_plot(sv, X_va, max_display=30)
```
TreeExplainer is exact and fast for tree ensembles; for other models use `shap.Explainer(model.predict_proba, masker)` (permutation / kernel methods), which is slower.

## Recursive elimination by SHAP
1. Fit, compute mean |SHAP| on validation data.
2. Remove the bottom 10-20% of features.
3. Refit and record CV score; repeat.
4. Choose the smallest set within noise of the best score.
Tools: `probatus.feature_elimination.ShapRFECV` implements this with CV; `BorutaSHAP` compares features against shuffled "shadow" copies using SHAP importance; `shap-select` fits a regression of the target on SHAP values and keeps significant features.

## Pitfalls
- **Importance is not usefulness**: a feature with large SHAP values can still hurt generalisation (it fits noise in training). Compute SHAP on held-out data, and confirm each elimination step with CV scores.
- **Correlated features** share credit; dropping one shifts its credit to the other. Group correlated features and evaluate groups.
- **Leakage**: if selection uses the validation data, report final performance on a separate test set or with nested CV.
- **Background data** for non-tree explainers changes values; use a representative sample (100-1000 rows).
- Interventional vs tree-path-dependent SHAP (`feature_perturbation`) can differ with correlated features; interventional with a background set is closer to "what the model does when this feature changes".

## When SHAP selection is worth it
Many features (hundreds+), tree models, and a need to explain why features were removed. For quick pruning, permutation importance or L1 may suffice.

## Verify
Plot CV score vs number of features retained; check that the selected set's SHAP rankings are stable across folds and seeds.
