---
id: computing-software.data-engineering.polars.polars-parse-dates-and-timezones
name: polars-parse-dates-and-timezones
category: computing-software
field: data-engineering
product: polars
tags: [polars-ts-parsing, polars-ts-timezones, to-date, to-datetime, time-zone, convert-time-zone, replace-time-zone, try-parse-dates]
level: practitioner
status: docs-checked
description: "Parse dates and datetimes in Polars from CSV or strings, handle mixed UTC offsets, and set or convert time zones."
sources:
  - https://docs.pola.rs/user-guide/transformations/time-series/parsing/
  - https://docs.pola.rs/user-guide/transformations/time-series/timezones/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get proper temporal dtypes and correct time zones.

**Dtypes.** `Date` (days since UNIX epoch, 32-bit signed int), `Datetime` (64-bit int since epoch, units ns/us/ms), `Duration` (created by subtracting Date/Datetime, like `timedelta`), `Time` (nanoseconds since midnight).

**From CSV:** `pl.read_csv("apple_stock.csv", try_parse_dates=True)`. This triggers schema inference over `infer_schema_length` rows (default 100), which is expensive with large values. Binary formats such as parquet have a schema that Polars respects.

**From strings:** pass the format to `str.to_date` (chrono strftime specification):

```python
df = pl.read_csv("apple_stock.csv", try_parse_dates=False)
df = df.with_columns(pl.col("Date").str.to_date("%Y-%m-%d"))
```

Extract features with `dt`: `pl.col("Date").dt.year().alias("year")`.

**Mixed offsets** (e.g. daylight-saving transitions): Polars parses them in UTC. Pass a target `time_zone` to `str.to_datetime`, or call `convert_time_zone` after:

```python
pl.Series(data).str.to_datetime("%Y-%m-%dT%H:%M:%S%z").dt.convert_time_zone("Europe/Brussels")
```

**Time zones.** A `Datetime` has one time zone only, so a column cannot hold several. Valid values: `None` (naive), `UTC`, or Area/Location names like `Asia/Kathmandu`. Do not use fixed offsets like +02:00. For multi-offset data the page suggests `utc=True` when parsing.

- `dt.replace_time_zone`: set, unset (`None`) or change the time zone
- `dt.convert_time_zone`: convert to another zone

```python
tz_naive = pl.Series("tz_naive", ["2021-03-27 03:00", "2021-03-28 03:00"]).str.to_datetime()
tz_aware = tz_naive.dt.replace_time_zone("UTC").rename("tz_aware")
pl.col("tz_aware").dt.replace_time_zone("Europe/Brussels")
pl.col("tz_aware").dt.convert_time_zone("Asia/Kathmandu")
pl.col("tz_aware").dt.replace_time_zone(None)
```

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/transformations/time-series/parsing/; https://docs.pola.rs/user-guide/transformations/time-series/timezones/. Corrected: Trimmed the replace_time_zone bullet to what the page states (set, unset with None, or change). Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
