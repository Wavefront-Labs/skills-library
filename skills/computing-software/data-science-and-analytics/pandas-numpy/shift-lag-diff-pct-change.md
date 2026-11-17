---
id: computing-software.data-science-and-analytics.pandas-numpy.shift-lag-diff-pct-change
name: shift-lag-diff-pct-change
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [shift-lag, pct-change, diff-series]
level: practitioner
status: gated
description: "Create lag features, period-over-period change and year-on-year growth with shift, diff and pct_change, per group."
sources:
  - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shift.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lags and growth
```python
df["prev"] = df.groupby("id")["v"].shift(1)
```
## Gotchas
- `DataFrame.shift(periods=1, freq=None, axis=0, fill_value, suffix=None)` shifts values; newly introduced missing values are NaN for numeric dtypes (NaT for datetimes) unless `fill_value` is set.
- Shift within groups (group first); a global shift leaks the previous entity's last value (reasoning from the shift definition).
- `diff()` and `pct_change(12)` (period count, for example 12 for yearly growth on monthly data) and the `fill_method` default: not confirmed on the page read (gated: unconfirmed, source is paywalled or blocked). Check the pandas reference for `DataFrame.diff` and `DataFrame.pct_change` for your version.

## Verify
- [ ] First row per group has NaN lag.

## Checked

2026-11-02. Confirmed against pandas.DataFrame.shift (signature, NaN/NaT fill default, fill_value). Gated: diff and pct_change behaviour including the fill_method default. The source was not read (those two reference pages were not fetched), not unreadable. Removed: the sort_values call.
Method: documentation only; no commands were run.
