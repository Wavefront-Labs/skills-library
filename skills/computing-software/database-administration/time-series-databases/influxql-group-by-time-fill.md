---
id: computing-software.database-administration.time-series-databases.influxql-group-by-time-fill
name: influxql-group-by-time-fill
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-influxql, influxql-group-by-time-fill, influxdb, flux]
level: practitioner
status: docs-checked
description: "Aggregate time series in InfluxQL with regular intervals and defined gap behaviour."
sources:
  - https://docs.influxdata.com/influxdb/v1/query_language/explore-data/
  - https://docs.influxdata.com/influxdb/v2/query-data/influxql/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/v1/dbrp/create/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InfluxQL GROUP BY time and fill

**Goal:** Aggregate time series in InfluxQL with regular intervals and defined gap behaviour.

## Steps
```
SELECT MEAN("value") FROM "temperature"
WHERE time >= now() - 24h AND "room" = 'lab'
GROUP BY time(5m), "room" fill(previous)
```
- `GROUP BY time(interval[,offset])` buckets by interval; add tags after for per-tag series.
- `fill(null|none|previous|linear|<number>)` controls empty buckets. A `GROUP BY time()` interval with no data reports `null` by default.
- Always bound time in WHERE; without it the default range runs from the minimum timestamp (1677-09-21) to `now()`.
- Append `tz('Europe/London')` to the query to return timestamps in that zone (UTC by default).
- In InfluxDB 2.x a bucket must be mapped to a database and retention policy (DBRP) before InfluxQL can query it (`influx v1 dbrp create`).

**Gotcha:** An aggregate over an unbounded time range returns epoch 0 (`1970-01-01T00:00:00Z`) as its timestamp, so bound time in `WHERE`.

## Verify
- Query returns one row per interval for the requested range.
- Fill setting visibly changes empty-bucket output.

## Checked

2026-11-03. Confirmed in the InfluxDB 1.x explore-data page (`GROUP BY time(interval,offset)`, `fill()` options, null default, default time range, `tz()`, epoch 0 for unbounded aggregates) and the v2 InfluxQL page and `influx v1 dbrp create` page (DBRP mapping). Removed: the selector-versus-aggregate timestamp claim, the 3.x native-support remark on this page and the unverified day-bucket alignment wording.
Method: documentation only; no commands were run.

