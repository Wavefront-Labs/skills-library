---
id: computing-software.data-science-and-analytics.experiment-design.regression-discontinuity-iv
name: regression-discontinuity-iv
category: computing-software
field: data-science-and-analytics
product: experiment-design
tags: [regression-discontinuity, instrumental-variables, two-stage-least-squares]
level: sme
status: draft
description: "Use a cutoff rule (RDD) or a valid instrument (2SLS) when randomisation is unavailable, and test the design assumptions."
sources:
  - https://mixtape.scunning.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RDD and IV
- RDD: compare units just above/below a cutoff using local linear regression within a bandwidth; check no manipulation of the running variable (density test) and covariate smoothness.
- IV: instrument z affects treatment, is as-good-as-random, and affects outcome only through treatment (exclusion). Estimate by 2SLS (for example `linearmodels.iv.IV2SLS`).
## Gotchas
- Weak instruments (first-stage F small) give biased, unstable estimates.
- The estimate is local (LATE), not the average effect for everyone.
## Verify
- [ ] First-stage strength reported; bandwidth sensitivity shown.
