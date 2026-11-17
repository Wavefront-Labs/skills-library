---
id: computing-software.database-administration.time-series-databases.influxdb3-sql-datafusion
name: influxdb3-sql-datafusion
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-v3, influxdb3-sql-datafusion, influxdb, flux]
level: practitioner
status: docs-checked
description: "Query InfluxDB 3 with SQL, which runs on Apache DataFusion over Arrow and Parquet."
sources:
  - https://docs.influxdata.com/influxdb3/core/reference/sql/
  - https://docs.influxdata.com/influxdb3/core/query-data/sql/
  - https://docs.influxdata.com/influxdb3/core/reference/sql/explain/
  - https://docs.influxdata.com/influxdb3/core/reference/sql/functions/time-and-date/
  - https://docs.influxdata.com/influxdb3/core/get-started/query/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InfluxDB 3 SQL and DataFusion

**Goal:** Query InfluxDB 3 with SQL, which runs on Apache DataFusion over Arrow and Parquet.

## Steps
- Tables replace measurements; tags and fields become columns; `time` is the timestamp column.
- Query: `SELECT date_bin(INTERVAL '5 minutes', time) AS bucket, host, avg(usage) FROM cpu WHERE time >= now() - INTERVAL '1 hour' GROUP BY 1, host ORDER BY 1`.
- Always filter on `time` so only relevant Parquet files are read.
- Use `EXPLAIN` to see the plan and `EXPLAIN ANALYZE` to execute it and view runtime metrics; `EXPLAIN ANALYZE VERBOSE` lists all scanned Parquet files.
- InfluxQL is also supported on InfluxDB 3.
- Flux is not supported in InfluxDB 3.

**Gotcha:** SQL has no implicit `GROUP BY time(...)`; use `date_bin` and group on its alias. To fill gaps use `date_bin_gapfill` with `interpolate` or `locf`, which requires time bounds in the `WHERE` clause.

## Verify
- `EXPLAIN` shows a time predicate in the plan.
- Result row counts match an equivalent Flux or InfluxQL query on v2 data.

## Checked

2026-11-03. Confirmed in the InfluxDB 3 Core SQL reference (DataFusion), the SQL query page and time-and-date functions page (`date_bin`, `date_bin_gapfill`, `interpolate`, `locf`), the EXPLAIN page (`EXPLAIN ANALYZE`, `VERBOSE`) and the get-started query page (Flux unsupported). Removed: the Flight SQL clients line, the InfluxQL edition-parity caveat and the file-pruning claim (not stated on the pages read).
Method: documentation only; no commands were run.

