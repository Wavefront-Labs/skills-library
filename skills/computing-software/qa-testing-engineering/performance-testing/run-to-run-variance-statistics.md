---
id: computing-software.qa-testing-engineering.performance-testing.run-to-run-variance-statistics
name: run-to-run-variance-statistics
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [run-variance, statistical-comparison, mann-whitney, performance-noise, confidence-intervals]
level: practitioner
status: verified
description: "Quantify run-to-run variance in performance tests and compare runs statistically: repeated runs, medians and MAD, bootstrap confidence intervals and Mann-Whitney tests."
sources:
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
  - https://en.wikipedia.org/wiki/Bootstrapping_(statistics)
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Run-to-run variance and statistical comparison

**Problem:** two runs of the same build differ by 5-15% in p95. Without knowing the noise, a "10% regression" may be nothing, and a real 5% regression goes unseen.

## Measure the noise
Run the identical test (same build, data, environment) 5-10 times. For each metric compute median and spread:
```python
import numpy as np
p95s = np.array([212, 205, 219, 230, 208, 214, 211])
median = np.median(p95s)
mad = np.median(np.abs(p95s - median))
cv = p95s.std(ddof=1) / p95s.mean()
print(median, mad, f"CV={cv:.1%}")   # 212.0 4.0 CV=3.9% for the sample above
```
The coefficient of variation guides thresholds. Rule of thumb (mine, not from a standard): a gate must sit above the noise band, so with CV around 4% a 10% gate is plausible, while a CV of 15% means fix the environment first.

## Compare two builds
Per-request latencies (from raw outputs) of run A vs run B:
```python
from scipy.stats import mannwhitneyu
stat, p = mannwhitneyu(a_latencies, b_latencies, alternative="less")   # is A faster than B? (small p when A's values tend to be lower)
```
Latency distributions are skewed and non-normal: prefer rank tests (Mann-Whitney U) or bootstrap over t-tests. With huge samples tiny differences become "significant": also require a practical effect size (e.g. median shift > 5%).

Bootstrap a confidence interval for the p95 difference:
```python
rng = np.random.default_rng(0)
diffs = [np.percentile(rng.choice(b, b.size), 95) - np.percentile(rng.choice(a, a.size), 95) for _ in range(2000)]
lo, hi = np.percentile(diffs, [2.5, 97.5])   # regression if lo > 0
```
On real Locust samples (about 600 requests per run, 5 users, local server): the same configuration compared with itself gave p = 0.097 once and p = 0.006 against another rerun (p95 23.5 vs 23.6 ms), so p-values alone flag noise; a +50 ms handler delay gave p = 3.6e-124 (`alternative="less"` for baseline vs slowed; `"greater"` gave 1.0), and the bootstrap CI of the p95 difference was [-0.4, +0.4] ms for the unchanged rerun and [49.5, 51.1] ms for the slowed run, which is the clearer signal.

## Reduce noise
Dedicated hosts, fixed CPU frequency/turbo settings, same data snapshot, warm-up excluded, generators isolated, avoid shared cloud bursts (burstable instances can change speed when CPU credits run out), run at the same time of day if the environment is shared.

## Gotchas
- Requests within a run aren't independent (shared state, GC periods); treat p-values as indicative and confirm with repeated runs.
- Comparing single runs is anecdote; compare medians of several runs.

## Verify
Gate thresholds are set above the measured noise band; A/A comparisons (same build twice) pass consistently.

## Checked
Python 3.14, NumPy and SciPy in a scratch venv; Locust 2.47.0 for the raw samples.
- Run: the variance snippet printed `212.0 4.0 CV=3.9%`; `mannwhitneyu` with `alternative='less'` and `'greater'` on real raw latencies (p-values quoted above); the bootstrap snippet (2000 resamples, seeded) produced the CIs quoted above for an unchanged rerun and a +50 ms run; a local test server with an adjustable delay supplied the samples.
- Fetched: SciPy `mannwhitneyu` page (URL live) and Wikipedia bootstrapping article (URL live). The unrelated Brendan Gregg KPTI link was dropped from sources because it does not support these claims.
