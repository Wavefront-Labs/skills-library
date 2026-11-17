---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.correlation-pearson-spearman
name: correlation-pearson-spearman
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [pearson-correlation, spearman-correlation, correlation-matrix, st-correlation]
level: intro
status: docs-checked
description: "Measure association with Pearson, Spearman or Kendall, build correlation matrices and avoid reading causation or nonlinearity into r."
sources:
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Correlation
```python
stats.spearmanr(x, y)
```
## Gotchas
- Spearman's coefficient is a nonparametric measure of monotonicity; it ranges from -1 to +1, and -1 or +1 imply an exact monotonic relationship.
- Plot the data as well as reading r.

## Verify
- [ ] Scatterplot reviewed alongside r.

## Checked

2026-11-02. Confirmed against scipy.stats.spearmanr (monotonic definition and range). Removed as not on the page read: pearsonr and kendalltau calls, df.corr(method=...), claims about Pearson and outliers, Anscombe, restricted range and confounders.
Method: documentation only; no commands were run.
