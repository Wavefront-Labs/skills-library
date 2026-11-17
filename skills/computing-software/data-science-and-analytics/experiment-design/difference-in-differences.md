---
id: computing-software.data-science-and-analytics.experiment-design.difference-in-differences
name: difference-in-differences
category: computing-software
field: data-science-and-analytics
product: experiment-design
tags: [difference-in-differences, parallel-trends, twfe-regression, causal-observational]
level: advanced
status: draft
description: "Estimate a policy or launch effect from treated and comparison groups before and after, and test the parallel-trends assumption."
sources:
  - https://mixtape.scunning.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Difference-in-differences
```python
m = smf.ols("y ~ treated * post + C(unit) + C(period)", data=df).fit(cov_type="cluster", cov_kwds={"groups": df["unit"]})
m.params["treated:post"]       # DiD estimate
```
Steps: plot pre-period trends for both groups; run an event-study with leads/lags; cluster SEs by unit.
## Gotchas
- Without parallel pre-trends the estimate is biased.
- With staggered adoption, two-way fixed effects can be biased; use modern estimators (for example Callaway-Sant'Anna) from specialist packages.
## Verify
- [ ] Lead coefficients near zero in the event study.
