---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.scipy-distributions-pdf-cdf-ppf
name: scipy-distributions-pdf-cdf-ppf
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [scipy-distributions, cdf-ppf-sf, binomial-poisson-normal, st-probability]
level: intro
status: docs-checked
description: "Compute probabilities, quantiles and tail areas with pdf/pmf, cdf, sf and ppf for normal, binomial, Poisson and other scipy distributions."
sources:
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binom.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.expon.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributions
```python
from scipy import stats
stats.norm.cdf(1.96); stats.norm.ppf(0.975)
stats.binom.pmf(3, n=10, p=0.5); stats.binom.sf(7, 10, 0.5)   # P(X>7)
stats.poisson.cdf(2, mu=4)
stats.t.ppf(0.975, df=19)
rv = stats.norm(loc=100, scale=15); rv.rvs(size=5, random_state=1)
```
## Gotchas
- `sf` is the survival function, defined as 1 - cdf but sometimes more accurate; `isf` is its inverse and `ppf` the inverse of `cdf`.
- Discrete distributions use `pmf(k, ...)` (binom, poisson); continuous ones use `pdf(x, ...)`.
- `expon` is parameterised by `scale`; the rate form with pdf = lambda * exp(-lambda * x) corresponds to `scale = 1 / lambda`.
- `lognorm` takes `s` as a shape parameter. If X is normal with mean mu and standard deviation sigma, then exp(X) is lognormal with `s = sigma` and `scale = exp(mu)`.
- `loc` and `scale` shift and scale every distribution; calling the distribution object, as in `stats.norm(loc=100, scale=15)`, gives a frozen object with the parameters fixed.
- `rvs` takes `size` and `random_state`.
## Verify
- [ ] `ppf(cdf(x))` returns x (the binom page checks this with np.allclose).

## Checked

2026-11-09. Confirmed against the scipy.stats norm, binom, poisson, t, expon and lognorm reference pages: method signatures (pdf, pmf, cdf, sf, ppf, isf, rvs with random_state), the sf description, expon scale = 1 / lambda, lognorm s and scale mapping, loc and scale semantics and frozen objects. Removed: the numeric comments after the first example line (not on the pages).
Method: docs-checked 2026-11-09 against the six scipy.stats distribution reference pages (method tables and notes read).
