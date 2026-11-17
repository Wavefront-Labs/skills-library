---
id: computing-software.data-science-and-analytics.pandas-numpy.memory-reduction-downcasting
name: memory-reduction-downcasting
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [memory-reduction, downcasting, category-dtype-memory]
level: practitioner
status: docs-checked
description: "Shrink memory by downcasting numerics, converting low-cardinality strings to category and selecting columns at read time."
sources:
  - https://pandas.pydata.org/docs/user_guide/scale.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reduce DataFrame memory
```python
df["n"] = pd.to_numeric(df["n"], downcast="integer")
df["f"] = pd.to_numeric(df["f"], downcast="float")
df["country"] = df["country"].astype("category")   # when unique values << rows
df.memory_usage(deep=True).sum() / 1e6              # MB
pd.read_csv(path, usecols=["a","b"])
```
## Gotchas
- The guide applies `category` to low-cardinality columns (few unique values relative to rows).
- `downcast="unsigned"`, `"integer"` and `"float"` pick the smallest fitting type; the guide shows float columns shrinking to float32.
- If data still does not fit, see the pandas scaling guide (for example `chunksize` when reading a single file).
## Verify
- [ ] Memory before/after measured with `deep=True`.

## Checked

Method: docs-checked 2026-11-09 against the pandas scaling to large datasets user guide (usecols, category, to_numeric downcast and memory_usage sections, read via text conversion). Dropped the high-cardinality size claim, the float32 precision advice and the assert_frame_equal check, and removed the dtype argument from read_csv, none of which that page confirms.
