---
id: computing-software.data-science-and-analytics.pandas-numpy.groupby-named-aggregation
name: groupby-named-aggregation
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [groupby-agg, named-aggregation, split-apply-combine, pd-groupby]
level: practitioner
status: docs-checked
description: "Summarise groups with groupby().agg using named aggregation, multiple functions and as_index control for clean flat results."
sources:
  - https://pandas.pydata.org/docs/user_guide/groupby.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# groupby + named aggregation
```python
out = (df.groupby(["region","month"], as_index=False, observed=True)
         .agg(revenue=("amt","sum"), orders=("id","nunique"), avg=("amt","mean")))
```
Named aggregation (`DataFrameGroupBy.agg`): the keywords are the output column names and the values are `(column, aggfunc)` tuples.
## Gotchas
- Groups with NaN keys are dropped by default; pass `dropna=False` to keep them.
- With categorical keys, `observed=False` returns the Cartesian product of all possible grouper values; `observed=True` keeps only the observed groups.
- `as_index=False` puts the group keys in columns instead of the index.
## Verify
- [ ] `out["revenue"].sum()` equals `df["amt"].sum()` (when no NaN keys).
## Checked
2026-11-02. Confirmed against the pandas user guide "Group by": named aggregation syntax, `as_index=False`, `dropna=False`, `observed`, and `nunique`. Removed: the unsourced note on averaging ratio columns.
Method: documentation only; no commands were run.
