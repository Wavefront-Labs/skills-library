---
id: computing-software.ai-ml-engineering.model-training.multi-seed-evaluation-and-run-variance
name: multi-seed-evaluation-and-run-variance
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, multi-seed-evaluation, run-to-run-variance, confidence-intervals, statistical-comparison, reporting]
level: practitioner
status: gated
description: "Measure run-to-run variance by training over several seeds, report mean with spread or intervals, and compare models with paired tests instead of single lucky runs."
sources:
  - https://arxiv.org/abs/2103.03098
  - https://arxiv.org/abs/2108.13264
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-seed evaluation and run-to-run variance

Fine-tuning and deep learning results vary with seed (initialisation, data order, dropout) by amounts often larger than the improvements being claimed. A single run per config can't distinguish them.

## How many seeds
- Minimum 3 for a rough spread; 5-10 for a claim; more for small datasets or unstable fine-tuning (BERT-style fine-tunes on small GLUE tasks vary several points) (rule-of-thumb counts and the GLUE spread not verified (gated: unconfirmed, source is paywalled or blocked)).
- Vary what's random in deployment retraining (init and data order), keep the test set fixed.
- Budget-constrained: fewer configs, more seeds per finalist (tune with 1 seed, confirm top 2-3 with 5+).

## Report
```python
import numpy as np, scipy.stats as st
scores = np.array([0.912, 0.905, 0.918, 0.899, 0.910])
mean, sd = scores.mean(), scores.std(ddof=1)
ci = st.t.interval(0.95, len(scores) - 1, loc=mean, scale=st.sem(scores))
print(f"{mean:.3f} +/- {sd:.3f} (95% CI {ci[0]:.3f}-{ci[1]:.3f}, n={len(scores)})")
# ran: 0.909 +/- 0.007 (95% CI 0.900-0.918, n=5)
```
Show all runs (dot or box plots), not only the max. "Best of N seeds" reporting inflates results and should be labelled as such if used.

## Compare two models
- **Paired by seed**: same seeds and data orders for A and B where possible; test the per-seed differences.
- Few seeds: report the mean difference and its interval; a Wilcoxon signed-rank or paired t-test over seeds (and/or over CV folds). With n = 5 pairs the smallest possible two-sided exact Wilcoxon p-value is 0.0625 and with n = 6 it is 0.03125 (computed with `scipy.stats.wilcoxon(..., method="exact")`), so a Wilcoxon test over 5 seeds can never reach p < 0.05; use more seeds or an interval on the mean difference.
- Account for test-set sampling too: bootstrap the test set per run, or use a paired test on per-example predictions (McNemar for accuracy) for a fixed pair of runs.
- Probability of improvement / "almost stochastic order" give more robust statements than p-values alone (attributed to Bouthillier et al., arXiv 2103.03098, "Accounting for Variance in Machine Learning Benchmarks"; the abstract does not mention these methods and the full text was not read (gated: unconfirmed, source is paywalled or blocked); arXiv 2108.13264 is Agarwal et al., on RL evaluation with interval estimates and performance profiles).
- Many configs compared: correct for multiple comparisons or confirm on a fresh split.

## Reduce variance itself
- Larger validation/test sets (sampling noise often dominates).
- Learning-rate warmup and lower LR for unstable fine-tunes; EMA/SWA weights.
- Ensembling seeds (for deployment) reduces variance of the final model.

## Gotchas
- Variance across CV folds mixes data variance with seed variance; vary one at a time when diagnosing.
- Early stopping on the test set (or picking best epoch per seed on test) biases results upward.
- Nondeterministic GPU runs with the same seed still vary; that variance is real too.

## Verify
Rerun the baseline with 5 seeds before claiming any gain; the improvement should exceed the baseline's seed spread and the paired interval should exclude 0.
