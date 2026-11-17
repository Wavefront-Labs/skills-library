---
id: computing-software.data-science-and-analytics.pandas-numpy.metric-definitions-kpi-tree
name: metric-definitions-kpi-tree
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [metric-definition, kpi-tree, north-star-metric]
level: intro
status: draft
description: "Write precise metric definitions (numerator, denominator, population, window) and decompose a headline KPI into drivers."
sources:
  - https://experimentguide.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Metric definitions
Document for each metric: name, formula, unit, grain, population, time window, source table, owner, known caveats.
Example: Weekly active users = distinct users with >=1 qualifying event in the ISO week (qualifying = list).
KPI tree: Revenue = visitors x conversion x average order value; analyse the weakest driver first.
## Gotchas
- Ratios of different populations; changing definitions silently breaks trends.
- Averages hide segments; check Simpson's paradox by splitting by key dimensions.
## Verify
- [ ] Two people compute the metric independently and match.
