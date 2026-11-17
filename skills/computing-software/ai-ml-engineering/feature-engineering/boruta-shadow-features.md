---
id: computing-software.ai-ml-engineering.feature-engineering.boruta-shadow-features
name: boruta-shadow-features
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, boruta, shadow-features, feature-selection, all-relevant-selection, random-forest]
level: practitioner
status: gated
description: "Select all-relevant features with Boruta: shadow feature permutation, iterations and p-values, BorutaPy/BorutaShap usage, tentative features, cost and leakage-safe use inside CV."
sources:
  - https://github.com/scikit-learn-contrib/boruta_py
  - https://www.jstatsoft.org/article/view/v036i11
  - https://scikit-learn.org/stable/modules/feature_selection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Boruta and shadow features

**Goal:** find **all** features carrying signal (all-relevant), not the minimal predictive subset. Useful for understanding drivers and pruning obviously useless columns from wide datasets.

## Algorithm
1. Copy every feature and shuffle the copies ("shadow" features: same distribution, no relationship to y).
2. Fit a random forest / boosting model on real + shadow features; compute importances.
3. A real feature scores a "hit" when its importance beats the best shadow feature.
4. Repeat; binomial tests mark features as confirmed, rejected, or tentative (gated: unconfirmed, source is paywalled or blocked).

## Usage
```python
# pip install boruta   (the PyPI package is `boruta`; run with 0.4.3, works with numpy 2.5 / scikit-learn 1.9)
from boruta import BorutaPy
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_jobs=-1, class_weight="balanced", max_depth=7)
bor = BorutaPy(rf, n_estimators="auto", perc=100, alpha=0.05, max_iter=100, random_state=0)
bor.fit(X_train.values, y_train.values)                # numpy arrays
confirmed = X_train.columns[bor.support_]
tentative = X_train.columns[bor.support_weak_]
```
- `perc=100` compares to the max shadow importance (strict); lower (e.g. 90) is more permissive.
- BorutaShap uses SHAP importances (more reliable than impurity importance, slower) (gated: unconfirmed, source is paywalled or blocked).

## Practical notes
- Cost: max_iter forest fits on a doubled feature matrix; subsample rows or limit depth for big data.
- Impurity-based importance favors high-cardinality numeric features; SHAP-based variants reduce this bias.
- Tentative features: decide with domain knowledge or more iterations.
- Correlated features are all kept (all-relevant), so Boruta does not remove redundancy; follow with correlation/VIF pruning if you need a compact set.

## Leakage
Running Boruta on the full dataset before CV leaks label information into feature choice. Run it inside each training fold (or on a separate selection split) and report performance on untouched data.

## Verify
- [ ] Model with confirmed features vs all features: CV score comparable or better; list of rejected features sanity-checked with domain experts.
