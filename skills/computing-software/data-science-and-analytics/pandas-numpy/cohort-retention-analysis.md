---
id: computing-software.data-science-and-analytics.pandas-numpy.cohort-retention-analysis
name: cohort-retention-analysis
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [cohort-analysis, retention-curve, cohort-pivot, product-analytics]
level: practitioner
status: draft
description: "Group users by first activity period and compute retention by period offset with pandas pivot tables."
sources:
  - https://pandas.pydata.org/docs/user_guide/reshaping.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cohort retention
```python
ev["cohort"] = ev.groupby("user")["ts"].transform("min").dt.to_period("M")
ev["period"] = (ev["ts"].dt.to_period("M") - ev["cohort"]).apply(lambda d: d.n)
t = ev.groupby(["cohort","period"])["user"].nunique().unstack(fill_value=0)
ret = t.div(t[0], axis=0)
```
## Gotchas
- Incomplete current periods look like drop-offs; mask them.
- Define "active" clearly; sign-up date and first-event date differ.
## Verify
- [ ] Period 0 retention is 100% for every cohort.
