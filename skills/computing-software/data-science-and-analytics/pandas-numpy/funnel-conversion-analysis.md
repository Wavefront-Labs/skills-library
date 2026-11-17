---
id: computing-software.data-science-and-analytics.pandas-numpy.funnel-conversion-analysis
name: funnel-conversion-analysis
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [funnel-analysis, step-conversion, time-to-convert]
level: practitioner
status: draft
description: "Count users reaching each ordered step within a window and report step-to-step conversion and time to convert."
sources:
  - https://pandas.pydata.org/docs/user_guide/groupby.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Funnel
```python
steps = ["view", "cart", "checkout", "paid"]
first = ev[ev.event.isin(steps)].pivot_table(index="user", columns="event", values="ts", aggfunc="min")
ok = first["view"].notna()
for a, b in zip(steps, steps[1:]):
    ok = ok & (first[b] >= first[a])              # order enforced
    print(b, ok.sum())
```
## Gotchas
- Without ordering and a time window, funnel counts overstate conversion.
- Count users, not events; dedupe bots and internal accounts.
## Verify
- [ ] Each step count is <= the previous step.
