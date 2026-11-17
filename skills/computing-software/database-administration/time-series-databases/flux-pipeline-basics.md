---
id: computing-software.database-administration.time-series-databases.flux-pipeline-basics
name: flux-pipeline-basics
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-flux, flux-pipeline-basics, influxdb, flux]
level: practitioner
status: docs-checked
description: "Write a correct Flux query with range, filter and aggregation in the efficient order."
sources:
  - https://docs.influxdata.com/flux/v0/stdlib/universe/range/
  - https://docs.influxdata.com/flux/v0/stdlib/universe/group/
  - https://docs.influxdata.com/flux/v0/stdlib/universe/yield/
  - https://docs.influxdata.com/influxdb/v2/query-data/optimize-queries/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/query/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flux pipeline basics

**Goal:** Write a correct Flux query with range, filter and aggregation in the efficient order.

## Steps
```
from(bucket: "sensors")
  |> range(start: -6h)
  |> filter(fn: (r) => r._measurement == "temperature" and r.room == "lab")
  |> filter(fn: (r) => r._field == "value")
  |> mean()
```
- Start with `range()` after `from()`, then place measurement, tag and field filters straight after it so they push down to storage.
- Data arrives as tables grouped by series; `group()` changes the grouping.
- Use `yield(name: "x")` to return several result sets.
- Run a script with `influx query --file query.flux`.

**Gotcha:** Once a non-pushdown function such as `map()` or `pivot()` runs, Flux pulls the data into memory and everything after it runs there, so keep filters ahead of it.

## Verify
- Running the query returns tables with `_time`, `_value`, `_field`, `_measurement`.

## Checked

2026-11-03. Confirmed in the optimize-queries page (pushdown behaviour, non-pushdown `map()` and `pivot()`), the Flux `range()`, `group()` and `yield()` pages and the `influx query` CLI page (`--file`). Removed: the claim that range lets the engine skip shards, `keep()`/`drop()` and Data Explorer wording, the full-scan claim for `group()`, and the scaling statement.
Method: documentation only; no commands were run.

