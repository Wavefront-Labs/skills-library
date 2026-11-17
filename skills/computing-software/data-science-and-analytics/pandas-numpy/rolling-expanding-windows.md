---
id: computing-software.data-science-and-analytics.pandas-numpy.rolling-expanding-windows
name: rolling-expanding-windows
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [rolling-window, expanding-window, ewm-smoothing]
level: practitioner
status: docs-checked
description: "Compute moving averages, expanding totals and exponentially weighted statistics, with min_periods and time-based windows set correctly."
sources:
  - https://pandas.pydata.org/docs/user_guide/window.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows
```python
s.rolling(7, min_periods=7).mean()
df.set_index("ts")["v"].rolling("7D").sum()       # time-based, needs sorted DatetimeIndex
s.expanding().max()
s.ewm(span=20, adjust=False).mean()
df.groupby("id")["v"].rolling(3).mean().reset_index(level=0, drop=True)
```
## Gotchas
- `min_periods` defaults to the window size for fixed windows (so the first n-1 rows are NaN) and to 1 for time-based windows.
- A time-based window such as `"7D"` needs a monotonic time index.
- `center=True` sets labels at the window centre, so each result uses values from after its row.
- `ewm` needs exactly one of `span`, `com`, `halflife` or `alpha`; `adjust=True` is the default.
## Verify
- [ ] Spot-check one window by hand with `s.iloc[i-6:i+1].mean()`.

## Checked

Method: docs-checked 2026-11-09 against the pandas windowing user guide (min_periods, time-based, centering, expanding and exponentially weighted sections, read via text conversion). The grouped rolling reset_index line is a standard idiom not shown on that page.
