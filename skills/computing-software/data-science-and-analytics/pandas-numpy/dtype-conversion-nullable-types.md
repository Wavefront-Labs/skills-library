---
id: computing-software.data-science-and-analytics.pandas-numpy.dtype-conversion-nullable-types
name: dtype-conversion-nullable-types
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [dtype-conversion, nullable-dtypes, convert-dtypes]
level: practitioner
status: draft
description: "Convert columns safely with astype, to_numeric and to_datetime, and adopt nullable Int64, boolean and string dtypes to keep missing values intact."
sources:
  - https://pandas.pydata.org/docs/user_guide/basics.html
  - https://pandas.pydata.org/docs/user_guide/integer_na.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dtype conversion and nullable types
```python
df["qty"] = pd.to_numeric(df["qty"], errors="coerce")      # bad strings -> NaN, inspect after
df["when"] = pd.to_datetime(df["when"], format="%Y-%m-%d", errors="coerce")
df["id"] = df["id"].astype("Int64")                       # capital I: allows <NA>
df["flag"] = df["flag"].astype("boolean")
df["name"] = df["name"].astype("string")
df = df.convert_dtypes()                                  # best-guess nullable dtypes
```
## Gotchas
- `errors="coerce"` hides bad data: count `isna()` before and after.
- `astype(int)` fails on NaN; use `Int64`.
- Always pass `format=` to `to_datetime` for speed and to avoid day/month ambiguity.
## Verify
- [ ] `df.dtypes` shows the intended types; NaN counts before and after conversion match expectations.
