---
id: computing-software.database-administration.time-series-databases.tsdb-downsampling-rollups
name: tsdb-downsampling-rollups
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-gen-downsampling, tsdb-downsampling-rollups]
level: practitioner
status: draft
description: "Design a raw-to-rollup retention ladder."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://docs.timescale.com/
  - https://docs.influxdata.com/influxdb/v2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Downsampling and rollups

**Goal:** Design a raw-to-rollup retention ladder.

## Steps
- Typical ladder: raw 7 to 30 days, 1-minute for 90 days, 1-hour for 2 years, 1-day forever.
- Store aggregates that re-aggregate: count, sum, min, max (avoid storing only mean); keep histograms as buckets or sketches.
- Implement per engine: Influx tasks with `aggregateWindow` and `to()`, Timescale continuous aggregates, Thanos compactor, Mimir recording rules, ClickHouse materialized views.
- Query routing: dashboards over long ranges read rollups; incident drill-down reads raw.
- Counters: roll up with `increase` or last value per window, not mean.
- Keep timestamps aligned to window start and document the convention.

**Gotcha:** Mean of means weights windows equally regardless of sample counts; carry sum and count instead.

## Verify
- Rollup sum over a closed day equals raw sum.
- Dashboards switch to rollups past a time threshold with no visible discontinuity.
