---
id: computing-software.data-science-and-analytics.pandas-numpy.loc-iloc-boolean-selection
name: loc-iloc-boolean-selection
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [loc-iloc, boolean-indexing, pandas-query, pd-indexing]
level: intro
status: docs-checked
description: "Select rows and columns with label-based loc, position-based iloc, boolean masks, isin and query."
sources:
  - https://pandas.pydata.org/docs/user_guide/indexing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# loc, iloc, masks
```python
df.loc[df["amt"] > 100, ["id","amt"]]
df.iloc[:5, 0:3]
df[(df.a > 1) & (df.b.isin(["x","y"]))]     # parentheses required around each condition
df.query("a < b and b < c")
```
## Gotchas
- `loc` slicing with labels includes both endpoints; `iloc` is purely integer-position based and raises `IndexError` for an out-of-range request.
- Combine boolean conditions with `&`, `|` and `~`, grouping each condition in parentheses; `query()` accepts both `and` and `&`.
- `isin` builds a mask for membership tests.
## Verify
- [ ] Result row count matches `mask.sum()`.

## Checked

Method: docs-checked 2026-11-09 against the pandas indexing user guide (loc/iloc, boolean grouping, isin and query sections, read via text conversion). Dropped the `@threshold` query variable and the single-call assignment advice, which were not confirmed.
