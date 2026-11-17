---
id: computing-software.data-engineering.apache-spark.timestamps-and-time-zones
name: timestamps-and-time-zones
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, pyspark, dataframe-api, spark-timestamps, session-timezone, timestamp-ntz, timestamp-ltz, to-timestamp, date-trunc, from-utc-timestamp, datetime-patterns, int96]
level: practitioner
status: docs-checked
description: "Get Spark dates and timestamps right: spark.sql.session.timeZone, TIMESTAMP vs TIMESTAMP_NTZ, parsing patterns, epoch conversions, date_trunc and DST-safe bucketing."
sources:
  - https://spark.apache.org/docs/latest/sql-ref-datatypes.html
  - https://spark.apache.org/docs/latest/sql-ref-datetime-pattern.html
  - https://spark.apache.org/docs/latest/configuration.html#runtime-sql-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timestamps and time zones in Spark

**Goal:** parse, store and bucket time values so results do not change with the cluster's time zone or DST.

## The two timestamp types
- `TIMESTAMP` (= `TIMESTAMP_LTZ`): an instant stored as UTC microseconds; displayed and parsed using `spark.sql.session.timeZone`.
- `TIMESTAMP_NTZ` (3.4+): wall-clock value with no zone; operations ignore time zones. Use for "local business time" columns that must not move.
- `TIMESTAMP` is an alias for one of the two; `spark.sql.timestampType` sets which (default `TIMESTAMP_LTZ`).

**Pin the session zone in every job:** `spark.conf.set("spark.sql.session.timeZone", "UTC")`. The default is the local time zone, so the same job can print different hours on a laptop vs cluster, and `to_date(ts)` can shift days. `UTC`, region IDs (`area/city`) and offsets are accepted; other short names are ambiguous.

## Parsing
```python
from pyspark.sql import functions as F
df = df.withColumn("ts", F.to_timestamp("ts_str", "yyyy-MM-dd'T'HH:mm:ss.SSSXXX"))
df = df.withColumn("d", F.to_date("d_str", "dd/MM/yyyy"))
df = df.withColumn("ts", F.timestamp_seconds("epoch_s"))        # or timestamp_millis
df = df.withColumn("epoch_s", F.unix_timestamp("ts"))
```
- Pattern letters are case sensitive: `MM` month vs `mm` minute, `yyyy` vs `YYYY` (week-based year, a classic late-December bug).
- Unparseable values become null (or raise under ANSI mode); count nulls after parsing. If upgrading from Spark 2 changes parse results, fix the patterns against the datetime pattern page.

## Converting zones
```python
F.from_utc_timestamp("ts_utc", "Australia/Sydney")   # shift instant into local wall time (for display/bucketing)
F.to_utc_timestamp("local_ts", "Australia/Sydney")   # local wall time -> UTC instant
F.convert_timezone("UTC", "America/New_York", "ts")
```
Use region IDs (`Australia/Sydney`), never fixed abbreviations (`EST`), so DST is applied.

## Bucketing
- `F.date_trunc("hour", "ts")`, `F.window("ts", "15 minutes")` bucket in the session zone.
- Daily business reporting in a local zone: convert to local first, then `to_date`. DST days have 23 or 25 hours; hourly series must not assume 24.

## Storage gotchas
- Parquet from old Hive/Impala writes INT96 timestamps and old calendars; if Spark raises a "rebase" error, look up the Parquet rebase-mode settings in the Spark SQL data sources docs before choosing a mode.
- Include an offset (`XXX`) in the write pattern for CSV/JSON so the zone is not lost.

## Verify
- [ ] Job sets `spark.sql.session.timeZone` explicitly.
- [ ] Running the job with a different JVM `-Duser.timezone` produces identical output.
- [ ] Null count after each `to_timestamp` is logged and expected.

## Checked
2026-10-31. Confirmed against the Spark configuration page and SQL data types page: `spark.sql.session.timeZone` default and accepted forms, `spark.sql.timestampType` default `TIMESTAMP_LTZ` (3.4.0), `TIMESTAMP_NTZ` semantics. Removed unconfirmed claims: INT96 rebase setting names, legacy parser policy, `convert_timezone` version, week-pattern rejection, toPandas tz behaviour.
Method: documentation only; no commands were run.
