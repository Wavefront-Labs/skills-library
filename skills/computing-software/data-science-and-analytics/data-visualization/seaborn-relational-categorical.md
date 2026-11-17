---
id: computing-software.data-science-and-analytics.data-visualization.seaborn-relational-categorical
name: seaborn-relational-categorical
category: computing-software
field: data-science-and-analytics
product: data-visualization
tags: [seaborn-scatterplot, catplot-facets]
level: practitioner
status: docs-checked
description: "Show relationships with scatter and line plots and split by facet using relplot and catplot grids."
sources:
  - https://seaborn.pydata.org/tutorial/relational.html
  - https://seaborn.pydata.org/tutorial/categorical.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relationships and facets
```python
import seaborn as sns
sns.scatterplot(data=df, x="x", y="y", hue="g")
sns.lineplot(data=df, x="day", y="v", hue="g", errorbar="sd")
sns.relplot(data=df, x="x", y="y", col="region", col_wrap=3, kind="scatter")
sns.catplot(data=df, x="day", y="v", col="region", kind="box")
```
## Gotchas
- `relplot()` is the figure-level function combining a FacetGrid with `scatterplot()` (`kind="scatter"`, the default) or `lineplot()` (`kind="line"`). `catplot()` does the same for the categorical axes-level functions (strip, swarm, box, violin, boxen, point, bar, count).
- `lineplot` aggregates repeated x values by default: it plots the mean with a 95% confidence interval computed by bootstrapping, which can be slow for large data. `errorbar=None` disables the interval, `errorbar="sd"` shows standard deviation, and `estimator=None` turns aggregation off.
- Adding `hue` to `lineplot` splits the plot into one line and error band per level.
- `swarmplot` (`kind="swarm"`) avoids overlapping points but only works well for relatively small datasets.
- `catplot(kind="bar")` applies an estimator (mean by default) and by default draws a bootstrapped 95% confidence interval as error bars; `errorbar=` selects other representations (since v0.12).
- Facet with `col`, `row` and `col_wrap`; the facet size is set by `height` and `aspect`.
## Verify
- [ ] Facets share axes unless deliberately free.

## Checked

2026-11-09. Confirmed against the seaborn relational and categorical tutorials (relplot/scatterplot/lineplot relationship, lineplot aggregation and errorbar options, estimator=None, swarm limits, catplot kinds, bar plot defaults, col_wrap, FacetGrid sizing). Both pages were searched by keyword. Removed: pairplot, the overplotting advice (alpha, hexbin), the shared-axes default claim and the statement about FacetGrid return types; the Verify item about shared axes stays as a manual check. Tags pairplot trimmed.
Method: docs-checked 2026-11-09 against the seaborn relational and categorical tutorial pages (keyword searched).
