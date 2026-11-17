---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.power-and-sample-size
name: power-and-sample-size
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [power-analysis, sample-size-calculation, minimum-detectable-effect]
level: practitioner
status: docs-checked
description: "Compute sample size or power for t-tests and proportions with statsmodels given effect size, alpha and power targets."
sources:
  - https://www.statsmodels.org/stable/generated/statsmodels.stats.power.TTestIndPower.solve_power.html
  - https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_effectsize.html
  - https://www.statsmodels.org/stable/stats.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Power
```python
from statsmodels.stats.power import TTestIndPower, NormalIndPower
TTestIndPower().solve_power(effect_size=0.3, alpha=0.05, power=0.8)   # nobs1: size of sample 1
from statsmodels.stats.proportion import proportion_effectsize
es = proportion_effectsize(0.12, 0.13)
NormalIndPower().solve_power(es, alpha=0.05, power=0.8)
```
## Gotchas
- `solve_power` solves for whichever one of `effect_size`, `nobs1`, `alpha`, `power`, `ratio` is `None`; exactly one must be `None`. To solve for `ratio` it must be passed explicitly as `None`, since its default is 1.
- The result is the size of sample 1; sample 2 has `ratio` times as many observations.
- `effect_size` is the standardised difference (difference between the two means divided by the standard deviation) and has to be positive.
- `proportion_effectsize(prop1, prop2)` uses the arcsine transform, `2 * (arcsin(sqrt(prop1)) - arcsin(sqrt(prop2)))`, and only `method="normal"` is implemented; the result can be negative, so check the sign convention before passing it on.
- `alternative` is `two-sided` by default; `larger` and `smaller` give one-sided tests.
- Effect size should come from what matters to the business, not from the pilot result.
## Verify
- [ ] Simulate the planned test at the computed n and confirm about 80% rejection under the assumed effect.

## Checked

2026-11-09. Confirmed against the statsmodels TTestIndPower.solve_power page (parameters, exactly-one-None rule, ratio, alternative, effect_size definition and positivity) and the proportion_effectsize page (signature, normal method only, arcsine formula). The statsmodels stats page lists NormalIndPower as the z-test power class that proportion effect sizes can be used with (read via the section index, not the class page). Removed: the claims about observed power and about dropout and clustering inflating n.
Method: docs-checked 2026-11-09 against the two statsmodels pages named above, read in full.
