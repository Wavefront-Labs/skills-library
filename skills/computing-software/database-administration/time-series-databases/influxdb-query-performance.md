---
id: computing-software.database-administration.time-series-databases.influxdb-query-performance
name: influxdb-query-performance
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-performance, influxdb-query-performance, influxdb, flux]
level: practitioner
status: docs-checked
description: "Speed up slow InfluxDB queries."
sources:
  - https://docs.influxdata.com/influxdb/v2/query-data/optimize-queries/
  - https://docs.influxdata.com/flux/v0/stdlib/profiler/
  - https://docs.influxdata.com/influxdb/v2/reference/config-options/
  - https://docs.influxdata.com/influxdb3/core/reference/sql/explain/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query performance

**Goal:** Speed up slow InfluxDB queries.

## Steps
- Start queries with pushdown functions: a narrow `range()` then filters on measurement, tag and field. Once a non-pushdown function runs, Flux pulls the data into memory and runs everything after it there.
- Keep `pivot()` and `map()` (non-pushdown) after the pushdown part; use `set()` instead of `map()` when setting a constant column value.
- Pre-aggregate for dashboards with tasks into rollup buckets and query those instead.
- Use the Flux profiler: `import "profiler"` with `option profiler.enabledProfilers = ["query", "operator"]`.
- Cap load with the `influxd` options `--query-concurrency`, `--query-queue-size` and `--query-memory-bytes`.
- For v3 SQL use `EXPLAIN ANALYZE` and time predicates.

**Gotcha:** A dashboard refreshing every few seconds over `range(start: -30d)` recomputes the full window each time; query rollups for long ranges.

## Verify
- With the `operator` profiler, storage-tier operations return as a single operation and later operations show their own statistics.

## Checked

2026-11-03. Confirmed in the optimize-queries page (pushdowns, memory behaviour, `set()` over `map()`, profilers), the Flux profiler page (`enabledProfilers`, `query` and `operator`), the `influxd` config options page (`query-concurrency`, `query-queue-size`, `query-memory-bytes`) and the InfluxDB 3 EXPLAIN page (`EXPLAIN ANALYZE`). Removed: the regex-filter, `limit()` and empty `group()` advice and the `ReadRange` operator name (not on the pages read).
Method: documentation only; no commands were run.

- Dashboard load time drops after switching to rollups.
