---
id: computing-software.database-administration.time-series-databases.flux-aggregatewindow
name: flux-aggregatewindow
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-flux, flux-aggregatewindow, influxdb, flux]
level: practitioner
status: docs-checked
description: "Aggregate a series into fixed windows, fill empty ones and emit evenly spaced points."
sources:
  - https://docs.influxdata.com/flux/v0/stdlib/universe/aggregatewindow/
  - https://docs.influxdata.com/flux/v0/stdlib/universe/fill/
  - https://docs.influxdata.com/flux/v0/stdlib/universe/derivative/
  - https://docs.influxdata.com/flux/v0/stdlib/universe/increase/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# aggregateWindow and downsampling

**Goal:** Aggregate a series into fixed windows, fill empty ones and emit evenly spaced points.

## Steps
```
from(bucket: "sensors")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "temperature")
  |> aggregateWindow(every: 5m, fn: mean, createEmpty: true)
  |> fill(usePrevious: true)
```
- `every` sets window size; `fn` is the aggregate to apply, for example `mean`, `max`, `last`, `sum` or `count`.
- `createEmpty: false` omits empty windows; `true` emits rows for empty windows that you can `fill()`.
- Window timestamps come from `timeSrc`, which defaults to `_stop`; set `timeSrc: "_start"` to label with the window start.
- `offset` shifts window boundaries (it can be negative); `period` sets the window length.
- `aggregateWindow()` needs `_start` and `_stop` columns, so call `range()` first.
- For counters, take `derivative(nonNegative: true)` or `increase()` rather than averaging the raw values.

**Gotcha:** If the `range()` boundaries do not align with window edges, the first or last window covers less than a full `every` and can look like a drop.

## Verify
- Row count equals range divided by `every`.
- Compare one window with a hand calculation of `mean`.

## Checked

2026-11-03. Confirmed in the Flux `aggregateWindow()` page (`every`, `period`, `offset`, `timeSrc` default `_stop`, `createEmpty`, needs `_start`/`_stop`), the `fill()` page (`usePrevious`), and the `derivative()` and `increase()` pages. Removed: the claim that the average of a counter is wrong as an absolute statement, and the local-day-boundary wording for `offset`.
Method: documentation only; no commands were run.

