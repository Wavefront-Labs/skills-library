---
id: computing-software.data-science-and-analytics.pandas-numpy.pivot-table-crosstab
name: pivot-table-crosstab
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [pivot-table, crosstab, pivot-margins, pd-reshape]
level: practitioner
status: docs-checked
description: "Build summary matrices with pivot_table and crosstab, including aggfunc, margins and fill_value, then flatten for export."
sources:
  - https://pandas.pydata.org/docs/user_guide/reshaping.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pivot_table / crosstab
```python
pt = df.pivot_table(index="region", columns="year", values="amt",
                    aggfunc="sum", margins=True, fill_value=0)
ct = pd.crosstab(df["a"], df["b"], normalize="index")
```
## Gotchas
- If the data contains duplicates, use `pivot_table()` (which aggregates) rather than `pivot()`.
- `margins=True` adds a row and column of partial group aggregates, labelled `All` in `crosstab`; drop them before further joins.
- `crosstab` defaults to a frequency table; `normalize` accepts `True`, `"index"` or `"columns"`.
## Verify
- [ ] Margin total equals `df["amt"].sum()`.

## Checked

Method: docs-checked 2026-11-09 against the pandas reshaping user guide (pivot, pivot_table margins and crosstab sections, read via text conversion). Dropped `observed=True`, which that page does not cover.
