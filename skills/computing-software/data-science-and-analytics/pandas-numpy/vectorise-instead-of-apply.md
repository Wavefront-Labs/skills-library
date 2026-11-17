---
id: computing-software.data-science-and-analytics.pandas-numpy.vectorise-instead-of-apply
name: vectorise-instead-of-apply
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [vectorization, avoid-iterrows, np-where-select, pd-performance]
level: practitioner
status: draft
description: "Replace row loops and row-wise apply with column arithmetic, np.where, np.select and map for orders-of-magnitude speed-ups."
sources:
  - https://pandas.pydata.org/docs/user_guide/enhancingperf.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vectorise
```python
import numpy as np
df["fee"] = np.where(df["amt"] > 100, df["amt"] * 0.02, 1.5)
df["tier"] = np.select([df.amt < 10, df.amt < 100], ["low","mid"], default="high")
df["region"] = df["code"].map(code_to_region)       # dict/Series lookup
```
## Gotchas
- `iterrows` returns copies and upcasts dtypes; `itertuples` is faster if a loop is truly needed.
- Measure with `%timeit` on realistic sizes before and after.
## Verify
- [ ] Vectorised result equals the loop result via `Series.equals`.
