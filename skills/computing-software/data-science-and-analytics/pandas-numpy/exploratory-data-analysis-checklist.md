---
id: computing-software.data-science-and-analytics.pandas-numpy.exploratory-data-analysis-checklist
name: exploratory-data-analysis-checklist
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [exploratory-data-analysis, eda-checklist, data-profiling, analysis-workflow-quality]
level: intro
status: draft
description: "Profile a new dataset systematically: grain, keys, types, ranges, missingness, distributions and relationships before modelling."
sources:
  - https://vita.had.co.nz/papers/tidy-data.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EDA checklist
1. Question and grain: what does one row represent?
2. Shape, dtypes, memory, key uniqueness.
3. Missingness by column and by time.
4. Ranges and impossible values (negative ages, future dates).
5. Distributions (hist/ECDF) and outliers.
6. Relationships (pair plots, grouped summaries).
7. Time coverage and gaps; reconciliation to a known total.
```python
df.describe(include="all").T; df.isna().mean(); df.duplicated().sum()
```
## Gotchas
- Row counts that silently change after joins are the most common error.
## Verify
- [ ] Reconcile at least one total against an independent source.
