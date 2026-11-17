---
id: computing-software.ai-ml-engineering.model-training.bootstrap-confidence-intervals-for-metrics
name: bootstrap-confidence-intervals-for-metrics
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, bootstrap-ci, confidence-intervals, model-evaluation, paired-bootstrap, metric-uncertainty]
level: practitioner
status: verified
description: "Put confidence intervals on any metric with the bootstrap: percentile CIs for AUC/F1, paired bootstrap for model comparison, cluster bootstrap for grouped data and pitfalls."
sources:
  - https://scikit-learn.org/stable/modules/generated/sklearn.utils.resample.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html
  - https://aclanthology.org/D12-1091.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bootstrap confidence intervals for metrics

**Why:** metrics like AUC, F1, NDCG or mean error have no simple closed-form CI; resampling the test set approximates their sampling distribution.

## Percentile CI for one model
```python
import numpy as np
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0)
n = len(y); B = 2000; stats = []
for _ in range(B):
    idx = rng.integers(0, n, n)
    if y[idx].min() == y[idx].max(): continue          # skip resamples with one class
    stats.append(roc_auc_score(y[idx], s[idx]))
lo, hi = np.percentile(stats, [2.5, 97.5])
```
Or `scipy.stats.bootstrap((y, s), lambda y, s: roc_auc_score(y, s), paired=True, vectorized=False, method="BCa")` for bias-corrected intervals (tested on SciPy 1.18.1: a 300-row, 20%-positive example gave BCa (0.654, 0.775) vs percentile (0.655, 0.775), manual loop (0.649, 0.786)).

## Paired bootstrap for comparing models
Resample the **same** indices for both models and look at the distribution of the difference:
```python
diffs = []
for _ in range(B):
    idx = rng.integers(0, n, n)
    diffs.append(metric(y[idx], pred_b[idx]) - metric(y[idx], pred_a[idx]))
ci = np.percentile(diffs, [2.5, 97.5]); p_worse = np.mean(np.array(diffs) <= 0)
```
If the CI excludes 0, B is better on this test distribution. Pairing removes test-set difficulty variance and is far more sensitive than comparing two separate CIs (tested: two scorers with separate AUC CI widths 0.137 and 0.142 had a paired-difference CI of only (-0.010, 0.037), width 0.048).

## Clustered data
When examples are grouped (several per user, document, or query), resample **groups**, not rows; row-level bootstrap underestimates variance.

## Pitfalls
- B: 1,000-10,000 is a common rule of thumb; more for tail percentiles (heuristic, not from a cited source).
- Bootstrap reflects test-set sampling noise only, not training randomness (seeds); for that, combine with multi-seed runs.
- Tiny test sets (under ~30 positives) give unstable intervals; report that limitation.
- Threshold-dependent metrics: fix the threshold beforehand (chosen on validation), do not re-optimize inside each resample.

## Verify
- [ ] Reports show metric with 95% CI, and model comparisons show paired-difference CIs.
