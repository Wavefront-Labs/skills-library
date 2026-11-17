---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.confidence-intervals-mean-proportion
name: confidence-intervals-mean-proportion
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [confidence-interval, proportion-confint, standard-error, st-intervals]
level: practitioner
status: docs-checked
description: "Build t-based intervals for means and Wilson intervals for proportions with scipy and statsmodels proportion_confint."
sources:
  - https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Confidence intervals
```python
n = len(x); se = x.std(ddof=1)/np.sqrt(n)
lo, hi = stats.t.interval(0.95, df=n-1, loc=x.mean(), scale=se)
from statsmodels.stats.proportion import proportion_confint
proportion_confint(count=45, nobs=200, alpha=0.05, method="wilson")
```
## Gotchas
- `proportion_confint` defaults to `method="normal"`. Other methods: `agresti_coull`, `beta` (Clopper-Pearson), `wilson`, `jeffreys`, `binom_test`. Pass `method` explicitly.
- Clopper-Pearson (`beta`) has coverage of at least 1-alpha but is in general conservative; most other methods have average coverage equal to 1-alpha and smaller coverage in some cases.
- `alternative` can be `two-sided`, `larger` or `smaller`; `count` and `nobs` must be integers for `binom_test`.
- `stats.t.interval(confidence, df, loc, scale)` is the equal-area interval around the median.
## Verify
- [ ] Simulate coverage: about 95% of repeated intervals contain the known truth.

## Checked

2026-11-09. Confirmed against the statsmodels proportion_confint page (signature, default method, method list, coverage notes, alternative values) and the scipy.stats.t page (interval signature, df, loc, scale). Removed: the interpretation of a 95% interval and the advice to use Wilson for small n or extreme proportions (neither stated on the pages read).
Method: docs-checked 2026-11-09 against the statsmodels proportion_confint page, read in full, and the scipy.stats.t method listing.
