---
id: computing-software.database-administration.time-series-databases.tsdb-metrics-wide-vs-narrow
name: tsdb-metrics-wide-vs-narrow
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-gen-schema, tsdb-metrics-wide-vs-narrow]
level: practitioner
status: draft
description: "Choose between wide and narrow layouts for application and infra metrics."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://docs.timescale.com/
  - https://docs.influxdata.com/influxdb/v2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wide versus narrow metric schemas

**Goal:** Choose between wide and narrow layouts for application and infra metrics.

## Steps
- Wide (one column per metric): fast multi-metric reads, better compression, requires schema change to add metrics. Fits stable sets (cpu, mem, disk).
- Narrow (name, value, labels): flexible and sparse, Prometheus and Influx model, but more rows and index entries.
- Hybrid: JSONB/map column for rare tags plus real columns for hot ones (Timescale, ClickHouse).
- Normalise dimensions with a lookup table of series ids (`series_id` to labels) when label text is large.
- Choose column types carefully: float32 vs float64, integers for counters, LowCardinality in ClickHouse for repeated strings.
- Index on `(series_id, time)` or the engine's sort key.

**Gotcha:** A narrow table with free-form label text per row stores the same strings billions of times; use ids or dictionary encoding.

## Verify
- Bytes per sample in the benchmark meet the target.
- Adding a metric needs no table rewrite (narrow) or an accepted migration (wide).
