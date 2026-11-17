---
id: computing-software.data-engineering.polars.polars-group-by-dynamic-rolling-and-resample
name: polars-group-by-dynamic-rolling-and-resample
category: computing-software
field: data-engineering
product: polars
tags: [polars-ts-rolling, group-by-dynamic, rolling, resampling, upsample, every-period, time-series]
level: practitioner
status: docs-checked
description: "Group Polars time series with group_by_dynamic (every, period, offset, truncate, closed), rolling windows, and resample by downsampling or upsampling."
sources:
  - https://docs.pola.rs/user-guide/transformations/time-series/rolling/
  - https://docs.pola.rs/user-guide/transformations/time-series/resampling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: aggregate time series into temporal windows.

**`group_by_dynamic`** groups rows into fixed windows. The data MUST be sorted ascending on the index column or the output will not be correct.

```python
df = pl.read_csv("apple_stock.csv", try_parse_dates=True).sort("Date")
df.group_by_dynamic("Date", every="1y").agg(pl.col("Close").mean())
```

Window parameters:
- `every`: how often windows start (e.g. `"2y"`, `"1y6mo"`, `"1mo"`, `"1d"`)
- `period`: window length; defaults to `every` when not given
- `offset`: shifts the window start

`every` need not equal `period`: `every="1d", period="2d"` gives windows overlapping by 1 day; `every="2d", period="1d"` leaves gaps, and points in gaps belong to no group.

`truncate` (default `True`): which datetime labels each group in the output. If the first point is 23 Feb 1981, `True` labels the first year 1 Jan 1981, `False` uses 23 Feb 1981. It affects only the displayed `Date`, not window boundaries.

Other options shown: `closed="left"` and `closed="both"`, `group_by="groups"` to combine with a normal group by, `include_boundaries=True`:

```python
df.group_by_dynamic(
    "time", every="1h", closed="both", group_by="groups", include_boundaries=True,
).agg(pl.len())
```

**`rolling`** is another entrance to group_by/agg, but windows are not fixed: they are determined by values in the `index_column`, e.g. `period="5d"` over dates {2021-01-06, 2021-01-10} gives windows ending at each date. The number of groups always equals the number of rows of the original frame.

**Resampling.** Downsampling (to lower frequency) is a special case of group by: use `group_by_dynamic` or `group_by_rolling`. Upsampling (to higher frequency) adds rows with nulls:

```python
df.upsample(time_column="time", every="15m").fill_null(strategy="forward")
```

Fill with a strategy or `interpolate()`; see the fill-null skill.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/transformations/time-series/rolling/; https://docs.pola.rs/user-guide/transformations/time-series/resampling/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
