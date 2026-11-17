---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.beta-binomial-conjugate
name: beta-binomial-conjugate
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [beta-binomial, conjugate-prior, credible-interval, st-bayesian]
level: practitioner
status: docs-checked
description: "Update a Beta prior with success and failure counts, then report credible intervals and the probability one variant beats another."
sources:
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.beta.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Beta-Binomial
```python
a0, b0 = 1, 1                                   # prior; justify it
post_A = stats.beta(a0 + 120, b0 + 880)
post_B = stats.beta(a0 + 150, b0 + 850)
post_A.interval(0.95)
```
## Gotchas
- `scipy.stats.beta` provides `rvs(a, b, loc=0, scale=1, size=1, random_state=None)` for random variates and `interval(confidence, a, b, ...)` for the equal-area interval around the median.
- The prior matters with small data; show sensitivity to two priors.

## Verify
- [ ] Posterior mean sits between prior mean and the observed rate.

## Checked

2026-11-02. Confirmed against scipy.stats.beta (rvs and interval signatures, random_state). The beta-binomial update (add successes to a, failures to b) is standard conjugacy arithmetic, shown with placeholder counts. Removed: the posterior comparison snippet using rng and the credible-interval interpretation sentence (neither on the page read).
Method: documentation only; no commands were run.
