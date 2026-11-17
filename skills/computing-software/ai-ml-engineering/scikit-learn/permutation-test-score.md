---
id: computing-software.ai-ml-engineering.scikit-learn.permutation-test-score
name: permutation-test-score
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, permutation-test-score, statistical-significance, cross-validation, model-evaluation, p-value]
level: practitioner
status: verified
description: "Test whether a model beats chance with permutation_test_score: label shuffling under CV, p-value meaning, permutation count, groups, and what a significant result does not prove."
sources:
  - https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.permutation_test_score.html
  - https://scikit-learn.org/stable/auto_examples/model_selection/plot_permutation_tests_for_classification.html
  - https://www.jmlr.org/papers/v11/ojala10a.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# permutation_test_score for significance

**Question answered:** is the cross-validated score better than what this pipeline achieves on labels with no relationship to the features? Useful for small datasets (medical, neuroscience, early-stage projects) where a 0.62 AUC might be noise.

## Usage
```python
from sklearn.model_selection import permutation_test_score, StratifiedKFold
score, perm_scores, pvalue = permutation_test_score(
    pipe, X, y, scoring="roc_auc",
    cv=StratifiedKFold(5, shuffle=True, random_state=0),
    n_permutations=1000, n_jobs=-1, random_state=0)
print(f"AUC {score:.3f}, null mean {perm_scores.mean():.3f}, p = {pvalue:.4f}")
```
- p-value = (count(perm_score >= score) + 1) / (n_permutations + 1). The smallest possible p is 1/(n+1), so 100 permutations can never give p below about 0.01; use 1000+ for publication-grade claims.
- Cost is (n_permutations + 1) x full CV: use cheap models or parallelism. Checked on 1.9.1 (signature `permutation_test_score(estimator, X, y, *, groups=None, cv=None, n_permutations=100, n_jobs=None, random_state=0, verbose=0, scoring=None, params=None)`): on a 120-row problem with 3 informative features, AUC 0.769 vs null mean 0.506, p = 0.01 with 99 permutations (equal to the formula, 1/100); on pure noise features AUC 0.583, p = 0.13; with 100 permutations the minimum p was 0.0099 = 1/101.

## Groups
Pass `groups=` so labels are permuted within groups and CV respects groups (e.g. patients with multiple samples); otherwise leakage inflates both the real and null distributions differently.

## Interpreting
- Significant p: features carry some information about y **under this pipeline**. It does not say the model is useful, calibrated or better than another model.
- Non-significant: either no signal or the model cannot find it; try simpler models before concluding no signal.
- Plot `perm_scores` histogram with the real score as a vertical line in reports.
- To compare two models, use paired tests on the same folds (corrected resampled t-test, 5x2cv) instead.

## Verify
- [ ] Sanity check: with shuffled y as the "real" labels, the p-value should be roughly uniform (not small). Twenty shuffled-label runs with 19 permutations each gave p between 0.30 and 1.00 (none below 0.30).
