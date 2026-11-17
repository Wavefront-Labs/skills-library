---
id: computing-software.data-science-and-analytics.pandas-numpy.deduplicate-records
name: deduplicate-records
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [drop-duplicates, duplicated-rows, key-uniqueness]
level: practitioner
status: docs-checked
description: "Identify duplicates by business key with duplicated, choose which row to keep deterministically, and assert key uniqueness afterwards."
sources:
  - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deduplicate
```python
df = df.drop_duplicates(subset=["email"], keep="last", ignore_index=True)
```
## Gotchas
- `drop_duplicates(subset=None, *, keep='first', inplace, ignore_index=False)`: by default every column is compared; `subset` limits it. `keep` is `'first'`, `'last'` or `False` (drop all duplicates).
- Which row survives depends on row order, so order the rows (for example by update time) before dropping.
- `subset` columns must be hashable or a `TypeError` is raised.
- Normalise (strip, lower) keys before comparing.

## Verify
- [ ] Check the key is unique after the drop.

## Checked

2026-11-02. Confirmed against pandas.DataFrame.drop_duplicates (signature, keep values, subset, ignore_index, hashable requirement). Removed: duplicated(), sort_values and is_unique calls (not on the page read), the assert example.
Method: documentation only; no commands were run.
