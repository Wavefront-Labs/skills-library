---
id: computing-software.database-administration.time-series-databases.flux-joins-and-pivot
name: flux-joins-and-pivot
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-flux, flux-joins-and-pivot, influxdb, flux]
level: practitioner
status: docs-checked
description: "Combine fields or measurements into one row per timestamp with pivot and join."
sources:
  - https://docs.influxdata.com/flux/v0/stdlib/universe/pivot/
  - https://docs.influxdata.com/flux/v0/stdlib/join/
  - https://docs.influxdata.com/flux/v0/stdlib/join/time/
  - https://docs.influxdata.com/flux/v0/stdlib/universe/join/
  - https://docs.influxdata.com/flux/v0/stdlib/universe/aggregatewindow/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flux join and pivot

**Goal:** Combine fields or measurements into one row per timestamp with pivot and join.

## Steps
- Pivot fields into columns: `|> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")`.
- Join two streams on `_time`: `import "join"` then `join.time(left: a, right: b, as: (l, r) => ({l with b_value: r._value}))`.
- The older `join(tables: {a: a, b: b}, on: ["_time", "host"])` is deprecated in favour of `join.inner()` and the `join` package.
- Align first: use `aggregateWindow` on both sides with the same `every` so timestamps match.
- Compute ratios after pivoting with `map()`, for example `|> map(fn: (r) => ({r with ratio: r.errors / r.total}))` (the pivoted field names become column names).

**Gotcha:** `pivot()` builds one new column per distinct `columnKey` value and one row per `rowKey`; if more than one value maps to the same row and column the result is ambiguous, so filter down to the series you need first.

## Verify
- Result has one row per timestamp with one column per field.
- No null columns caused by misaligned timestamps.

## Checked

2026-11-03. Confirmed in the Flux `pivot()` page (`rowKey`, `columnKey`, `valueColumn`, column naming), the `join.time()` page (joins exclusively on `_time`, `as` function) and the `join()` page (deprecated in favour of `join.inner()`, `tables`/`on` form). Removed: the claims that the old join is slower and that pivoting high-cardinality tags exhausts memory (not stated).
Method: documentation only; no commands were run.

