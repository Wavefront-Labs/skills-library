---
id: computing-software.database-administration.time-series-databases.influxdb-tasks-downsampling
name: influxdb-tasks-downsampling
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-tasks, influxdb-tasks-downsampling, influxdb, flux]
level: practitioner
status: docs-checked
description: "Schedule a Flux task that rolls raw data into a long-retention bucket."
sources:
  - https://docs.influxdata.com/influxdb/v2/process-data/common-tasks/downsample-data/
  - https://docs.influxdata.com/influxdb/v2/process-data/task-options/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/task/create/
  - https://docs.influxdata.com/flux/v0/stdlib/influxdata/influxdb/to/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tasks for downsampling

**Goal:** Schedule a Flux task that rolls raw data into a long-retention bucket.

## Steps
```
option task = {name: "downsample_1h", every: 1h, offset: 5m}
from(bucket: "raw") |> range(start: -task.every)
  |> filter(fn: (r) => r._measurement == "cpu")
  |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
  |> to(bucket: "rollup_1y", org: "myorg")
```
- Create with `influx task create --file task.flux`; list with `influx task list`.
- `offset` delays execution (for example a `10m` offset runs an hourly task 10 minutes after the hour) to account for data that arrives late.
- Use `range(start: -task.every)` so each run covers one interval; re-writing a point with the same measurement, tag set and timestamp merges into the existing point rather than adding a new one.
- Schedule downsampling tasks to run before data passes the source bucket's retention period.
- Backfill past data with a one-off query using `to()` over the missing range.

**Gotcha:** `every` and `cron` are mutually exclusive task options; with no `offset`, points that arrive after a run starts are missed.

## Verify
- `influx task run list --task-id <id>` shows successful runs.
- Rollup bucket receives points at each interval.

## Checked

2026-11-03. Confirmed in the downsample-data page (task with `option task`, `aggregateWindow`, `to()`, offset for late data, retention scheduling), the task-options page (`every`, `cron`, `offset`), the `influx task create` page (`-f/--file`) and the line-protocol duplicate-point rule. Removed: the claim that the target bucket needs longer retention, and the one-off `to()` backfill instruction.
Method: documentation only; no commands were run.

