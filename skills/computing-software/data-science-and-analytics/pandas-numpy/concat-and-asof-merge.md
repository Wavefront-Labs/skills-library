---
id: computing-software.data-science-and-analytics.pandas-numpy.concat-and-asof-merge
name: concat-and-asof-merge
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [pandas-concat, merge-asof, append-frames]
level: advanced
status: docs-checked
description: "Stack frames with concat (ignore_index, keys) and join on nearest time with merge_asof for tick, event or price lookups."
sources:
  - https://pandas.pydata.org/docs/user_guide/merging.html#merge-ordered-and-merge-asof
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# concat and merge_asof
```python
all_ = pd.concat([a, b], keys=["a","b"], ignore_index=False, sort=False)
q = pd.merge_asof(trades, quotes, on="time", by="ticker", tolerance=pd.Timedelta("2ms"))
```
## Gotchas
- `merge_asof` matches on the nearest key rather than an equal key; both DataFrames must be sorted by the key. `by` adds a group-wise match and `tolerance` limits how far a match may be.
- `concat` on mismatched columns fills NaN (outer join); `join="inner"` takes the intersection of the axis values.
- `concat` makes a full copy of the data: collect frames in a list and concat once rather than concatenating iteratively.
## Verify
- [ ] Unmatched asof rows show NaN; tolerance excludes stale matches.
## Checked
2026-11-02. Confirmed against the pandas user guide "Merge, join, concatenate and compare": `concat` with `keys`, `ignore_index`, `sort=False`, `join="inner"`, the copy warning, and `merge_asof` with `by`, `tolerance`, and the sorted-key requirement. Removed: the `direction` argument and the numeric/datetime key claim (not stated on the page).
Method: documentation only; no commands were run.
