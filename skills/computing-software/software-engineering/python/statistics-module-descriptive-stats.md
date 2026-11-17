---
id: computing-software.software-engineering.python.statistics-module-descriptive-stats
name: statistics-module-descriptive-stats
category: computing-software
field: software-engineering
product: python
tags: [python, py-numbers, statistics-module, mean, median, stdev, quantiles, correlation, fmean]
level: practitioner
status: docs-checked
description: "Compute mean, median, mode, variance, quantiles, correlation and linear regression with the statistics module and pick fmean, stdev or pstdev correctly."
sources: ["https://docs.python.org/3/library/statistics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# statistics module

```python
import statistics as st
data = [2.5, 3.1, 4.7, 5.0, 9.9]

st.fmean(data)            # fast float mean; st.mean keeps Fraction/Decimal types exact
st.median(data); st.median_low(data); st.median_high(data)
st.mode([1, 1, 2]); st.multimode([1, 1, 2, 2])        # multimode returns a list (3.8+)
st.stdev(data)            # SAMPLE standard deviation (n-1)
st.pstdev(data)           # POPULATION standard deviation (n)
st.quantiles(data, n=4, method="exclusive")           # quartile cut points
st.correlation(x, y); st.linear_regression(x, y)      # 3.10+: returns slope, intercept
st.NormalDist(mu=100, sigma=15).cdf(115)              # normal distribution helper
```

## Choosing
- Float data: `fmean` is the fast floating-point mean; `mean` keeps `Decimal` and `Fraction` types.
- Samples vs populations: `stdev`/`variance` for samples, `pstdev`/`pvariance` for the full population. Mixing them is the most common error.
- Skewed data: report `median` and quantiles, not just mean.

## Gotchas
- Empty input raises `StatisticsError`; `stdev` needs at least two points.
- `quantiles` default method is "exclusive" (for samples from a larger population); pass `method="inclusive"` for population data or samples known to include the extremes.
- `mode` of multi-modal data returns the first mode since 3.8, earlier versions raised an error.
- `correlation` raises if either input is constant.
- NaN values give surprising results in order statistics (`median`, `mode`, `quantiles`); strip them first, e.g. with `math.isnan`.

## Verify
- [ ] Cross-check a sample against a known worked example (e.g. `stdev([2,4,4,4,5,5,7,9]) ≈ 2.138`, `pstdev == 2.0`).
- [ ] Tests cover empty and single-element input.

## Checked

- 2026-11-03: checked against the CPython docs `library/statistics.rst`: `fmean` (3.8), `multimode` (3.8), `mode` returning the first mode since 3.8, `quantiles` methods, `correlation`/`linear_regression` (3.10) and their constant-input `StatisticsError`, `stdev` needing two points, empty input errors, NaN warning, `NormalDist`.
- Removed: NumPy and spreadsheet comparisons.

Method: documentation only; no commands were run.
