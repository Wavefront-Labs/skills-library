---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.summary-statistics-robust
name: summary-statistics-robust
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [descriptive-statistics, robust-statistics, outlier-iqr, st-descriptive]
level: intro
status: docs-checked
description: "Report centre, spread and shape with median, MAD and IQR alongside mean and SD using scipy.stats."
sources:
  - https://docs.scipy.org/doc/scipy/reference/stats.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.iqr.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.median_abs_deviation.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skew.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kurtosis.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Robust summaries
```python
from scipy import stats
stats.describe(x, ddof=1)
stats.iqr(x); stats.median_abs_deviation(x, scale="normal")
stats.trim_mean(x, 0.1)
stats.skew(x), stats.kurtosis(x)
```
## Gotchas
- `stats.iqr` uses the 25th to 75th percentile range by default (`rng=(25, 75)`) and divides the result by `scale` (default 1.0).
- `median_abs_deviation(scale="normal")` divides by the inverse standard normal quantile function at 0.75, about 0.67449, so it estimates the standard deviation for normal data.
- `stats.kurtosis` uses Fisher's definition by default (normal gives 0.0); `fisher=False` gives Pearson's (normal gives 3.0).
- `stats.skew` is the Fisher-Pearson coefficient of skewness; `bias=False` applies the bias correction.
- `stats.describe` takes `ddof`, and `trim_mean` returns the mean after trimming a fraction of extreme values.
- State your outlier rule explicitly; a rule flags points, it does not justify deleting them.
## Verify
- [ ] Plot a histogram next to the numbers.

## Checked

2026-11-09. Confirmed against the scipy.stats iqr, median_abs_deviation, skew and kurtosis reference pages (signatures, defaults, scale and Fisher/Pearson definitions) and the scipy.stats overview listing for describe (ddof) and trim_mean. Removed: the 1.5 x IQR fence formula, the claims about how mean and SD respond to outliers, and the numpy percentile and std calls (not on the pages read).
Method: docs-checked 2026-11-09 against the four scipy reference pages and the scipy.stats overview listing.
