---
id: computing-software.ux-hci-design.ux-research-methods.task-metrics-and-confidence-intervals
name: task-metrics-and-confidence-intervals
category: computing-software
field: ux-hci-design
product: ux-research-methods
tags: [task-success-rate, adjusted-wald-interval]
level: advanced
status: draft
description: "Report completion rates with adjusted-Wald intervals and time with geometric means for small samples."
sources:
  - https://measuringu.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Small-sample metrics
- Completion rate: use the adjusted Wald interval (add z^2/2 successes and z^2 trials; z=1.96 for 95 percent) rather than the normal approximation for small n.
- Task time is right-skewed: report the geometric mean or median, compute CI on log times.
- Satisfaction: SEQ (7-point, per task), SUS (per test).
- Compare to a benchmark with a one-sample test or interval.

```python
def adj_wald(x,n,z=1.96):
    p=(x+z*z/2)/(n+z*z); se=(p*(1-p)/(n+z*z))**.5; return p-z*se,p+z*se
```

## Verify
- [ ] 5 of 5 successes gives a lower bound well under 100 percent, not 100.
