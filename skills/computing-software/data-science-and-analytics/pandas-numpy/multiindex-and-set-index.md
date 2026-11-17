---
id: computing-software.data-science-and-analytics.pandas-numpy.multiindex-and-set-index
name: multiindex-and-set-index
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [multiindex, set-index, xs-cross-section]
level: practitioner
status: docs-checked
description: "Use set_index, MultiIndex, xs and reset_index to get hierarchical lookups, then flatten back when exporting."
sources:
  - https://pandas.pydata.org/docs/user_guide/advanced.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MultiIndex
```python
m = df.set_index(["region","month"]).sort_index()
m.loc["EU"]; m.loc[("EU","2026-01")]
m.xs("2026-01", level="month")
m.reset_index()
```
## Gotchas
- Indexing a MultiIndex that is not lexsorted is inefficient (PerformanceWarning) and can raise `UnsortedIndexError`; call `sort_index()` first.
- Flatten column MultiIndex: `df.columns = ["_".join(map(str,c)) for c in df.columns]`.
## Verify
- [ ] `m.index.is_monotonic_increasing` is True before slicing.

## Checked

Method: docs-checked 2026-11-09 against the pandas advanced indexing user guide (sorting, xs and lexsort sections, read via text conversion). Dropped the join-by-level-name claim, and the column-flattening idiom is standard Python not shown on that page.
