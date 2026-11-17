---
id: computing-software.data-science-and-analytics.pandas-numpy.explode-and-json-normalize
name: explode-and-json-normalize
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [explode-lists, json-normalize, nested-json-flatten]
level: practitioner
status: docs-checked
description: "Flatten list columns with explode and nested JSON with json_normalize so nested API data becomes analysable rows."
sources:
  - https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html
  - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.explode.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Explode and json_normalize
```python
df = df.explode("tags", ignore_index=True)
flat = pd.json_normalize(records, record_path=["items"], meta=["order_id", ["cust", "id"]], sep="_")
```
## Gotchas
- `explode` replicates the other columns' values (index values are duplicated), so aggregate afterwards carefully.
- Empty list-likes give a NaN for that row; scalars are returned unchanged; the result dtype of exploded rows is object.
- `json_normalize(data, record_path, meta, meta_prefix, record_prefix, errors='raise', sep='.', max_level)`: `meta` is a list of paths, each a str or list of str; `errors='ignore'` skips meta keys that are missing.
- Row order is non-deterministic when exploding sets.

## Verify
- [ ] Sum of list lengths (empty lists count as one row) equals row count after explode.

## Checked

2026-11-02. Confirmed against pandas.DataFrame.explode and pandas.json_normalize reference pages (signatures, defaults, empty-list NaN, meta path forms, sep). The example records and column names are placeholders.
Method: documentation only; no commands were run.
