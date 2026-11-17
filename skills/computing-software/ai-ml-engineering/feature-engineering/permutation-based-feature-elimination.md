---
id: computing-software.ai-ml-engineering.feature-engineering.permutation-based-feature-elimination
name: permutation-based-feature-elimination
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, permutation-feature-selection, permutation-importance, feature-elimination, model-agnostic, feature-selection]
level: practitioner
status: verified
description: "Select features by permutation importance on held-out data: repeated permutations, elimination loops with refits, thresholds against noise and handling correlated features."
sources:
  - https://scikit-learn.org/stable/modules/permutation_importance.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.inspection.permutation_importance.html
  - https://explained.ai/rf-importance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Permutation-based feature elimination

Permutation importance = drop in a validation metric when one feature's values are shuffled. Model-agnostic and measured on held-out data, so it reflects generalisation, unlike impurity importance.

## Measure
```python
from sklearn.inspection import permutation_importance
model.fit(X_tr, y_tr)
r = permutation_importance(model, X_va, y_va, scoring="roc_auc", n_repeats=20, random_state=0, n_jobs=-1)
imp = pd.DataFrame({"mean": r.importances_mean, "std": r.importances_std}, index=X_va.columns).sort_values("mean")
```
- Use the validation fold, not training data (training importance rewards overfitting).
- Pass a Pipeline and raw columns to measure importance of original features, not transformed ones.

## Elimination loop
```python
features = list(X.columns)
while True:
    scores, imps = [], []
    for tr, va in cv.split(X, y):
        m = clone(model).fit(X.iloc[tr][features], y.iloc[tr])
        scores.append(roc_auc_score(y.iloc[va], m.predict_proba(X.iloc[va][features])[:, 1]))
        imps.append(permutation_importance(m, X.iloc[va][features], y.iloc[va], scoring="roc_auc", n_repeats=10, random_state=0).importances_mean)
    imp = pd.Series(np.mean(imps, axis=0), index=features)
    drop = imp[imp <= 0].index.tolist()          # features whose shuffling does not hurt (or helps)
    if not drop: break
    features = [f for f in features if f not in drop]
```
In a test with 2 informative and 6 noise features, `imp <= 0` dropped four noise columns in round 1 but two noise columns survived by chance (importance slightly above 0), so use the `mean - 2*std` rule below rather than the bare `<= 0` test.

Track CV score each round; stop if it drops beyond noise. Remove features in small batches (refit after each), because importances change once correlated partners are removed.

## Thresholds against noise
- Compare each importance with its std across repeats and folds; drop if `mean - 2*std <= 0`.
- Add random noise columns (`np.random.randn`) as probes: drop features not more important than the best probe (like Boruta).

## Correlated features caveat
Two correlated useful features can both show near-zero permutation importance (each covers for the other). Eliminating both loses signal. Cluster correlated features first and permute groups, or eliminate one at a time with refits.

## Leakage and selection bias
The selection loop uses validation data; the final CV score after selection is optimistic. Use nested CV or a separate final test set.

## Cost
Each round needs fits x folds plus permutations x features. For large feature sets, prefilter with cheap methods (variance, mutual information, L1), then use permutation elimination on the shortlist.
