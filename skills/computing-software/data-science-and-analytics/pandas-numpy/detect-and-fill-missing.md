---
id: computing-software.data-science-and-analytics.pandas-numpy.detect-and-fill-missing
name: detect-and-fill-missing
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [missing-values, fillna, isna-audit, pd-missing]
level: practitioner
status: docs-checked
description: "Audit NaN patterns by column, then drop, fill or interpolate deliberately, documenting each imputation choice."
sources:
  - https://pandas.pydata.org/docs/user_guide/missing_data.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Missing values
```python
df.isna().mean().sort_values(ascending=False)     # share missing per column
df.dropna(subset=["id"])
df["x"] = df["x"].fillna(df["x"].median())
df["x"] = df.groupby("g")["x"].transform(lambda s: s.fillna(s.median()))
df["t"] = df["t"].interpolate(method="time")      # needs DatetimeIndex
```
## Gotchas
- Detect missing values with `isna()` or `notna()` (both treat `None` as missing); to check a value against `pd.NA` use `isna()` rather than equality.
- Convert sentinel values such as -999 or "N/A" to real missing values first.
- `interpolate(method="time")` interpolates by the time index; `"values"` and spline methods also exist.
## Verify
- [ ] Missing share before/after documented; no sentinel values remain.

## Checked

Method: docs-checked 2026-11-09 against the pandas missing data user guide (detection, NA comparison and interpolate sections, read via text conversion). Dropped `dropna(thresh=)`, the train/test leakage advice and the indicator-column suggestion, which that page does not state.
