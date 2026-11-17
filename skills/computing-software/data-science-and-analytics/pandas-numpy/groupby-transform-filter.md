---
id: computing-software.data-science-and-analytics.pandas-numpy.groupby-transform-filter
name: groupby-transform-filter
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [groupby-transform, groupby-filter, groupby-rank]
level: practitioner
status: docs-checked
description: "Add group-level features back onto rows with transform, drop groups with filter and rank or take top-n within groups."
sources:
  - https://pandas.pydata.org/docs/user_guide/groupby.html#transformation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# transform / filter / rank
```python
df["share"] = df["amt"] / df.groupby("region")["amt"].transform("sum")
big = df.groupby("cust").filter(lambda g: len(g) >= 5)
df["rk"] = df.groupby("region")["amt"].rank(method="dense", ascending=False)
top3 = df.sort_values("amt", ascending=False).groupby("region").head(3)
```
## Gotchas
- `transform` must return a result the same size as the group chunk or broadcastable to it (a scalar works); `agg` collapses each group instead.
- `transform` with a user-defined function is often less performant than the built-in methods; prefer string names such as `"sum"`.
- `filter` takes a function returning a boolean per group; the groupby user guide demonstrates it with `len(x) > 2` style tests.
## Verify
- [ ] Shares sum to 1.0 within each group.

## Checked

Method: docs-checked 2026-11-09 against the pandas groupby user guide (transform, filter and rank sections read via text conversion). The `rank(method="dense")` and `head(3)` calls are standard API; the guide lists `rank()` and shows `head`, but the dense option itself was not confirmed on that page.
