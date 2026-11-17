---
id: computing-software.ai-ml-engineering.model-training.checking-split-distribution-match
name: checking-split-distribution-match
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, covariate-shift-check, adversarial-validation, distribution-shift, data-splits, psi, ks-test]
level: practitioner
status: draft
description: "Check that train, validation and test splits share a distribution: per-feature tests, PSI, adversarial validation classifiers, label balance and what to do on mismatch."
sources:
  - https://scikit-learn.org/stable/modules/cross_validation.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html
  - https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Checking split distribution match (covariate shift)

A validation score only predicts production performance if validation looks like production. Check splits before trusting any metric.

## 1. Label and key segment balance
```python
for name, d in {"train": tr, "val": va, "test": te}.items():
    print(name, len(d), d.y.mean().round(4), d.segment.value_counts(normalize=True).round(3).to_dict())
```
Large differences in base rate or segment mix change metrics directly (precision depends on base rate).

## 2. Per-feature comparison
- Numeric: two-sample KS (`scipy.stats.ks_2samp`), compare quantiles; with large n everything is "significant", so look at effect size (KS statistic > ~0.1 deserves a look).
- Categorical: frequency tables, chi-square, share of unseen categories in val/test.
- **PSI** (population stability index) per feature with deciles from train:
```python
def psi(a, b, bins=10):
    q = np.unique(np.quantile(a, np.linspace(0, 1, bins + 1)))
    pa = np.histogram(a, q)[0] / len(a) + 1e-6; pb = np.histogram(np.clip(b, q[0], q[-1]), q)[0] / len(b) + 1e-6
    return np.sum((pa - pb) * np.log(pa / pb))
```
Rule of thumb: < 0.1 stable, 0.1-0.25 moderate, > 0.25 large shift.

## 3. Adversarial validation (multivariate)
Train a classifier to tell train rows from test rows:
```python
X = pd.concat([tr[feats], te[feats]]); z = np.r_[np.zeros(len(tr)), np.ones(len(te))]
auc = cross_val_score(HistGradientBoostingClassifier(), X, z, cv=5, scoring="roc_auc").mean()
```
- AUC ~0.5: indistinguishable. AUC >> 0.5: shift; the classifier's top features (permutation importance) are the shifted ones (timestamps, IDs, drifting measurements).

## What to do on mismatch
- **Time-dependent data**: shift is expected; use a time-based split so validation mimics the future, rather than shuffling it away.
- **Leaky identifiers** (IDs, timestamps encoding split): drop them from features.
- **Test reflects production, train does not**: build validation from the train rows most similar to test (highest adversarial probability), or reweight training rows by `p/(1-p)` from the adversarial model (importance weighting).
- **Accidental split bug** (sorted data then head/tail split): reshuffle or stratify.

## Verify
Record split stats (sizes, base rates, PSI summary, adversarial AUC) with the experiment so later comparisons know the evaluation conditions.
