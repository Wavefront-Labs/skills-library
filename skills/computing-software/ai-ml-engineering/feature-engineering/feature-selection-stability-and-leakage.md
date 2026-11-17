---
id: computing-software.ai-ml-engineering.feature-engineering.feature-selection-stability-and-leakage
name: feature-selection-stability-and-leakage
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, feature-selection, selection-stability, stability-selection, bootstrap-selection, selection-bias]
level: practitioner
status: draft
description: "Check whether selected features are stable across resamples (Jaccard, stability selection), avoid selection bias from selecting outside CV, and report selection honestly."
sources:
  - https://arxiv.org/abs/0809.2932
  - https://jmlr.org/papers/v18/17-514.html
  - https://www.pnas.org/doi/10.1073/pnas.102102699
  - https://scikit-learn.org/stable/common_pitfalls.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Feature selection stability and leakage

**Goal:** know whether your "important features" are a real finding or an artefact of one data split, and keep selection from inflating scores.

## Measure stability
Run the selector on bootstrap samples or CV folds and compare the chosen sets:
```python
from itertools import combinations
sets = []
for tr, _ in RepeatedStratifiedKFold(n_splits=5, n_repeats=4, random_state=0).split(X, y):
    sel = clone(selector).fit(X.iloc[tr], y.iloc[tr])
    sets.append(set(X.columns[sel.get_support()]))
jacc = np.mean([len(a & b) / len(a | b) for a, b in combinations(sets, 2)])
freq = pd.Series([f for s in sets for f in s]).value_counts() / len(sets)
```
- Mean pairwise Jaccard near 1 = stable; below ~0.5 = the specific list is largely noise. Nogueira et al. (2018) propose a corrected stability measure with confidence intervals.
- `freq` per feature: selection probability across resamples.

## Stability selection (Meinshausen & Buhlmann)
Run a sparse selector (e.g. L1 with randomised penalties) on many subsamples of half the data; keep features selected in more than a threshold fraction (e.g. 60-80%). Provides error control on false selections and is far more reliable than one lasso fit for "which features matter" questions.

## Why lists are unstable
Correlated features substitute for each other; small samples; weak signals. The prediction may be equally good with different sets - instability matters mainly when someone interprets the list (scientific claims, business explanations) or pays per feature.

## Leakage: selection bias
Selecting features on the full dataset and then cross-validating the model on those features overstates accuracy - dramatically on wide data (Ambroise & McLachlan, 2002). Selection must be inside each training fold; the reported score must come from data the selector never saw.

## Reporting
Report: the selection procedure, stability metric, per-feature selection frequency, and performance from nested CV/test. Avoid claims like "feature X drives churn" from a single unstable selection.

## Verify
- [ ] Stability (Jaccard or Nogueira index) reported with the selected list.
- [ ] Selection happens within training folds only.
- [ ] Interpretive claims limited to features with high selection frequency.
