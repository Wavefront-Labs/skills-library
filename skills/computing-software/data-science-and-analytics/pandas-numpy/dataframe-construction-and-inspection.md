---
id: computing-software.data-science-and-analytics.pandas-numpy.dataframe-construction-and-inspection
name: dataframe-construction-and-inspection
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [dataframe-construction, dataframe-inspection, pandas-info-describe, pd-structures]
level: intro
status: draft
description: "Create DataFrames from dicts, records and arrays, then inspect shape, dtypes, memory and summary statistics before doing any analysis."
sources:
  - https://pandas.pydata.org/docs/user_guide/dsintro.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Build and inspect a DataFrame
```python
import pandas as pd
df = pd.DataFrame({"id": [1, 2, 3], "price": [9.5, 3.2, None]})
df = pd.DataFrame.from_records(list_of_dicts)
df.shape; df.dtypes; df.head(); df.tail()
df.info(memory_usage="deep")        # non-null counts, dtypes, true memory incl. strings
df.describe(include="all")          # numeric by default; include="all" adds object columns
df.nunique(); df.isna().sum()
```
## Gotchas
- A column mixing numbers and None becomes float64 (NaN); integer columns with missing values need the nullable `Int64` dtype.
- `describe()` silently skips non-numeric columns unless `include` is set.
- `info()` without `memory_usage="deep"` underestimates object-column memory.
## Verify
- [ ] Every column dtype matches what you expect before any transformation.
- [ ] Row count equals the source record count.
