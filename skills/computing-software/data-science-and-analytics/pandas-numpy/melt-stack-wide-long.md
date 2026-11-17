---
id: computing-software.data-science-and-analytics.pandas-numpy.melt-stack-wide-long
name: melt-stack-wide-long
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [melt-wide-to-long, stack-unstack, wide-to-long]
level: practitioner
status: docs-checked
description: "Tidy wide data with melt, wide_to_long, stack and unstack so each variable is a column and each observation a row."
sources:
  - https://pandas.pydata.org/docs/user_guide/reshaping.html#reshaping-by-melt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wide to long
```python
long = df.melt(id_vars=["id"], var_name="quarter", value_name="sales")
```
`melt` unpivots a wide DataFrame so that columns named in `id_vars` stay as identifiers and the other columns become two columns, "variable" and "value"; `var_name` and `value_name` rename those two.
## Gotchas
- Without `var_name`/`value_name` the new columns are called `variable` and `value`.
- `pivot()` can only handle unique rows specified by index and columns; with duplicates use `pivot_table()`.
## Verify
- [ ] Long row count = wide rows x melted columns.
## Checked
2026-11-02. Confirmed against the pandas user guide "Reshaping and pivot tables": `melt`, `id_vars`, `var_name`, `value_name`, and the `pivot` vs `pivot_table` note. Removed: `wide_to_long`, `value_vars`, and the `unstack` ValueError claim (not shown on the page).
Method: documentation only; no commands were run.
