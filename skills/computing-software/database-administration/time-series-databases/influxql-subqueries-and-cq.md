---
id: computing-software.database-administration.time-series-databases.influxql-subqueries-and-cq
name: influxql-subqueries-and-cq
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-influxql, influxql-subqueries-and-cq, influxdb, flux]
level: practitioner
status: docs-checked
description: "Chain aggregations with InfluxQL subqueries and know what replaced continuous queries in 2.x."
sources:
  - https://docs.influxdata.com/influxdb/v1/query_language/explore-data/
  - https://docs.influxdata.com/influxdb/v1/query_language/continuous_queries/
  - https://docs.influxdata.com/influxdb/v2/process-data/common-tasks/downsample-data/
  - https://docs.influxdata.com/influxdb3/core/plugins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subqueries and continuous queries

**Goal:** Chain aggregations with InfluxQL subqueries and know what replaced continuous queries in 2.x.

## Steps
- Subquery: `SELECT MAX(m) FROM (SELECT MEAN("value") AS m FROM "cpu" GROUP BY time(1m), "host") WHERE time > now() - 1h GROUP BY time(1h)`.
- The outer query selects from the inner query's result, for example `SELECT SUM("max") FROM (SELECT MAX("water_level") FROM "h2o_feet" GROUP BY "location")`.
- 1.x continuous queries: `CREATE CONTINUOUS QUERY cq_1h ON db BEGIN SELECT MEAN(v) INTO "rp_long"."cpu_1h" FROM "cpu" GROUP BY time(1h),* END`.
- A CQ query needs no time range in its `WHERE` clause; at each run it covers the previous interval (an hourly CQ at 8:00 queries `time >= '7:00' AND time < '8:00'`).
- In 2.x replace CQs with Flux tasks that use `aggregateWindow` and `to()` (see the downsample-data page).
- In InfluxDB 3 the Processing Engine runs Python plugins on a schedule.

**Gotcha:** A CQ with `GROUP BY time(1h)` covers only the previous interval at run time, so points written for an older interval afterwards are not picked up by that run.

## Verify
- Target measurement gets one new point per interval.
- Rolled-up counts match the raw data for a closed hour.

## Checked

2026-11-03. Confirmed in the 1.x explore-data page (subquery examples), the 1.x continuous-queries page (`CREATE CONTINUOUS QUERY ... BEGIN ... END`, `INTO`, previous-interval execution), the v2 downsample-data page (`aggregateWindow`, `to()`) and the InfluxDB 3 Processing Engine page (scheduled triggers). Removed: the per-series execution-order claim, the manual `SELECT INTO` backfill instruction and the scheduled-SQL option.
Method: documentation only; no commands were run.

