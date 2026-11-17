---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.distribution-fitting-qq
name: distribution-fitting-qq
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [qq-plot, distribution-fit, normality-check]
level: practitioner
status: docs-checked
description: "Compare data with candidate distributions using Q-Q plots, fitted parameters and normality tests, remembering large-sample tests flag trivial deviations."
sources:
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distribution checks
```python
stats.probplot(x, dist="norm", plot=ax)
stats.shapiro(x)
```
## Gotchas
- `probplot(x, sparams=(), dist='norm', fit=True, plot=None, rvalue=False)` plots sample data against theoretical quantiles (normal by default) and can fit a line.
- `shapiro`: for N > 5000 the W statistic is accurate but the p-value may not be.

## Verify
- [ ] Q-Q points track the line in the middle and tails you care about.

## Checked

2026-11-02. Confirmed against scipy.stats.probplot and scipy.stats.shapiro (signature, 5000 limit). Removed: norm.fit/lognorm.fit lines, advice about large-n rejection and normal residuals (not on the pages read).
Method: documentation only; no commands were run.
