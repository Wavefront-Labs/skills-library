---
id: computing-software.ai-ml-engineering.scikit-learn.partial-dependence-and-ice-plots
name: partial-dependence-and-ice-plots
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, partial-dependence, ice-plots, partialdependencedisplay, model-inspection, feature-effects]
level: practitioner
status: verified
description: "Use scikit-learn partial dependence and ICE plots to show how predictions change with a feature, spot interactions and avoid misreading them under correlated features."
sources:
  - https://scikit-learn.org/stable/modules/partial_dependence.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.inspection.PartialDependenceDisplay.html
  - https://christophm.github.io/interpretable-ml-book/pdp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partial dependence and ICE plots

**Partial dependence (PD)**: average prediction as one (or two) features are varied over a grid, others held at their observed values. **ICE**: one curve per row (PD is their average).

## Plot
```python
from sklearn.inspection import PartialDependenceDisplay, partial_dependence
PartialDependenceDisplay.from_estimator(
    model, X_val, features=["age", "income", ("age", "income")],
    kind=["both", "both", "average"],   # per feature: "average" (PD), "individual" (ICE), "both"; 2-way pairs must be "average"
    centered=True,                # c-ICE: all curves start at 0, easier to see heterogeneity
    subsample=300, grid_resolution=50, percentiles=(0.05, 0.95), random_state=0)
res = partial_dependence(model, X_val, ["age"], kind="average")   # raw arrays
```
- A single `kind="both"` with a 2-way pair raises `ValueError: ICE plot cannot be rendered for 2-way feature interactions ... should be configured to use kind=['both', 'both', 'average'] explicitly` (1.9.1), hence the list above.
- Classifiers: `response_method="auto"` means PD on `predict_proba` when the `brute` method runs, but tree models that use `method="recursion"` (HistGradientBoosting, RandomForest, DecisionTree) only support `decision_function` (log-odds for HGB): `response_method="predict_proba"` raises `With the 'recursion' method, the response_method must be 'decision_function'` unless you pass `method="brute"`. A random forest has no `decision_function`, so its recursion PD is in probability units. Multiclass: `partial_dependence` returns one curve per class (shape `(3, 100)` for 3 classes) and has no `target=`; `PartialDependenceDisplay.from_estimator(..., target=k)` picks the class to plot.
- The default `grid_resolution` is 100 (`average` array shape `(1, 100)`); `kind="both"` adds `individual` of shape `(1, n_rows, 100)`.
- Categorical features: pass `categorical_features=[...]` for bar-style plots.
- Pipelines work directly; features are named by input column.
- `percentiles` clips the grid to dense regions; don't read curves outside the data.

## Reading them
- Flat PD with fanning ICE curves: the feature matters but through interactions (effects cancel on average). Look at 2-way PD or colour ICE by another feature.
- Parallel ICE curves: additive effect; PD summarises it well.
- Monotonic constraints should show monotonic ICE for every row.
- The y-scale is the model's output, so compare to the prediction range for importance.

## The correlated-features trap
PD evaluates combinations that don't exist (age 20 with 30 years of work experience) when features correlate. Curves then reflect extrapolation. Alternatives:
- **ALE plots** (accumulated local effects): use only local, realistic changes. Python packages: `alibi` and `PyALE` (both exist on PyPI, checked with `pip index versions`).
- Restrict to subsets where the combination is plausible.
- Check with a 2D histogram of the feature pair.

## Causal caution
PD shows what the model does, not what happens in the world if you change the feature. Don't present PD as an intervention effect without a causal design.

## Performance
Tree-based models in sklearn (`HistGradientBoosting*`, `DecisionTree*`, RF with `method="recursion"`, chosen by `auto`) compute PD fast (0.002-0.003 s for HGB/RF on 1500 rows vs 0.28-0.34 s with `brute`); `method="brute"` evaluates the model on the whole dataset per grid point: subsample `X` for big data.

## Verify
For a feature with a known effect (simulated or business-known), the PD direction and magnitude should match; ICE heterogeneity should align with known segments.
