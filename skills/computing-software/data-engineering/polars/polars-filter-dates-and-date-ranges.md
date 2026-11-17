---
id: computing-software.data-engineering.polars.polars-filter-dates-and-date-ranges
name: polars-filter-dates-and-date-ranges
category: computing-software
field: data-engineering
product: polars
tags: [polars-ts-filter, filter, is-between, datetime, date-range, negative-dates, time-series]
level: practitioner
status: docs-checked
description: "Filter Polars date and datetime columns by a single date, a range with is_between, or negative (BCE) dates using the dt namespace."
sources:
  - https://docs.pola.rs/user-guide/transformations/time-series/filter/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: select rows by date in a Polars DataFrame.

Filtering date columns works like any other column via `.filter`. Polars uses Python's native `datetime`, `date` and `timedelta` for equality comparisons against `pl.Datetime`, `pl.Date` and `pl.Duration`. Note the lowercase `datetime` method (Python) versus the uppercase `Datetime` data type.

Setup (Apple stock prices):

```python
from datetime import datetime
df = pl.read_csv("apple_stock.csv", try_parse_dates=True)
```

**Single date** (equality):

```python
df.filter(pl.col("Date") == datetime(1995, 10, 16))
```

**Date range** with `is_between(start, end)`:

```python
df.filter(pl.col("Date").is_between(datetime(1995, 7, 1), datetime(1995, 11, 1)))
```

**Negative dates.** For archaeological data, Polars can parse and store negative dates, but the Python `datetime` library cannot represent them. Filter using attributes of the `.dt` namespace instead:

```python
ts = pl.Series(["-1300-05-23", "-1400-03-02"]).str.to_date()
negative_dates_df = pl.DataFrame({"ts": ts, "values": [3, 4]})
negative_dates_df.filter(pl.col("ts").dt.year() < -1300)
```

If the column is still text, first convert it with `str.to_date` (see the parsing skill), then compare using `dt.year()` and similar accessors.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/transformations/time-series/filter/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
