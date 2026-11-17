---
id: computing-software.data-science-and-analytics.experiment-design.srm-sample-ratio-check
name: srm-sample-ratio-check
category: computing-software
field: data-science-and-analytics
product: experiment-design
tags: [sample-ratio-mismatch, srm-chi-square, experiment-data-quality, ab-analysis]
level: practitioner
status: draft
description: "Run a chi-square goodness-of-fit on assignment counts and halt analysis when the split deviates from design."
sources:
  - https://experimentguide.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SRM check
```python
from scipy import stats
obs = [50210, 49210]; exp = np.array([0.5, 0.5]) * sum(obs)
chi2, p = stats.chisquare(obs, exp)       # p < 0.001 -> investigate, do not trust results
```
Common causes: redirects, bot filtering applied unevenly, crashes in one variant, logging loss, bucketing bugs.
## Gotchas
- Use a strict threshold (for example p<0.001) since the check runs on every experiment.
- A "small" imbalance at huge n is still a real bug.
## Verify
- [ ] Result recorded in the experiment report before the metric read-out.
