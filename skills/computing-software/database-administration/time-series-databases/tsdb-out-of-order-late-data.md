---
id: computing-software.database-administration.time-series-databases.tsdb-out-of-order-late-data
name: tsdb-out-of-order-late-data
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-gen-selection, tsdb-out-of-order-late-data]
level: practitioner
status: draft
description: "Handle late, duplicate and out-of-order samples per engine."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://docs.timescale.com/
  - https://docs.influxdata.com/influxdb/v2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Out-of-order and late data

**Goal:** Handle late, duplicate and out-of-order samples per engine.

## Steps
- Prometheus: rejects out-of-order by default; enable `storage.tsdb.out_of_order_time_window: 30m` (2.39+, confirm) to accept recent late samples.
- InfluxDB: accepts any timestamp within retention; same series plus timestamp overwrites; backfill creates old shards.
- TimescaleDB: inserts into any chunk allowed, compressed chunks slower; use `ON CONFLICT`.
- ClickHouse: ReplacingMergeTree dedups on merge only; query with `FINAL` or `argMax`.
- Design idempotent writers with deterministic keys so retries do not duplicate.
- Capture event time and ingest time to measure lateness; alert on p99 lateness.
- Rollups must either recompute late windows (refresh with lookback) or stay append-only.

**Gotcha:** Rollups with a refresh window shorter than the lateness silently omit late data.

## Verify
- A test replay of a late batch changes the expected aggregate once.
- Lateness metric stays under the refresh window.
