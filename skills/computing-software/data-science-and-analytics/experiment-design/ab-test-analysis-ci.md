---
id: computing-software.data-science-and-analytics.experiment-design.ab-test-analysis-ci
name: ab-test-analysis-ci
category: computing-software
field: data-science-and-analytics
product: experiment-design
tags: [ab-test-analysis, relative-lift-ci, delta-method]
level: practitioner
status: draft
description: "Estimate lift with a confidence interval, report absolute and relative effects and use user-level variance for ratio metrics."
sources:
  - https://experimentguide.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conversion test read-out
```python
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep
cnt = [1260, 1340]; n = [20000, 20000]
z, p = proportions_ztest(cnt, n)
lo, hi = confint_proportions_2indep(cnt[1], n[1], cnt[0], n[0], compare="diff")
rel = (cnt[1]/n[1]) / (cnt[0]/n[0]) - 1
```
Report: baseline rate, absolute difference + CI, relative lift, p, n, dates, and guardrail outcomes.
## Gotchas
- Relative lift CIs are wider than they look when baseline is small.
- Avoid segment fishing; label post-hoc segments as exploratory.
## Verify
- [ ] Recompute the headline from raw counts in a second tool.
