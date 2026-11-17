---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.bootstrap-intervals
name: bootstrap-intervals
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [bootstrap-ci, percentile-bootstrap, scipy-bootstrap]
level: practitioner
status: docs-checked
description: "Estimate intervals for medians, ratios and other awkward statistics by resampling with scipy.stats.bootstrap, choosing BCa where suitable."
sources:
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bootstrap
```python
res = stats.bootstrap((x,), np.median, confidence_level=0.95,
                      n_resamples=9999, method="BCa", random_state=1)
res.confidence_interval
```
## Gotchas
- `scipy.stats.bootstrap` takes the data as a sequence of samples, a statistic, `confidence_level`, `n_resamples` and `method` (including `'BCa'`); `random_state` fixes the seed for reproducibility.
- The result exposes `confidence_interval`.
- Resample the unit of independence (for example customers, not rows).

## Verify
- [ ] Interval stable across two different seeds.

## Checked

2026-11-02. Confirmed against scipy.stats.bootstrap (parameters confidence_level, n_resamples, method BCa, random_state, confidence_interval result). Removed: statements about extremes and small samples (not on the page read).
Method: documentation only; no commands were run.
