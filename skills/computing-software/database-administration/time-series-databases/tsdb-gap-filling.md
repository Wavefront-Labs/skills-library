---
id: computing-software.database-administration.time-series-databases.tsdb-gap-filling
name: tsdb-gap-filling
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-gen-downsampling, tsdb-gap-filling]
level: practitioner
status: draft
description: "Present regular series from irregular or missing samples without lying about the data."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://docs.timescale.com/
  - https://docs.influxdata.com/influxdb/v2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gap filling and interpolation

**Goal:** Present regular series from irregular or missing samples without lying about the data.

## Steps
- Decide semantics per signal: gauge (carry forward last value for a bounded time), counter (compute rate then fill zeros if appropriate), event (zero fill).
- Tools: Influx `aggregateWindow(createEmpty: true)` plus `fill()`, InfluxQL `fill(previous|linear|0)`, Timescale `time_bucket_gapfill` with `locf` and `interpolate`, Prometheus staleness plus `last_over_time(x[10m])`, ClickHouse `WITH FILL`.
- Bound carry-forward (for example locf for max 15 minutes) so outages show as missing, not flat lines.
- Mark synthetic points in output (`is_filled` column) for downstream analytics.
- Do not interpolate counters across resets.

**Gotcha:** Unbounded last-observation-carried-forward hides sensor outages by drawing a flat healthy line.

## Verify
- Chart shows gaps for dead devices after the cap.
- Filled row count equals expected buckets.
