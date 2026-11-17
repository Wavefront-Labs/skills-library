---
id: computing-software.database-administration.influxdb.task-options-and-scheduling
name: task-options-and-scheduling
category: computing-software
field: database-administration
product: influxdb
tags: [tasks, flux, task-options, every, cron, offset]
level: practitioner
status: docs-checked
description: "Set Flux task options: name, every or cron, and offset, with the scheduling rule that every-based tasks first run at the next interval boundary."
sources:
  - https://docs.influxdata.com/influxdb/v2/process-data/task-options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Every task declares an `option task` record:

```js
option task = {name: "downsample-cpu", every: 1h, offset: 5m}
```

- `name`: required.
- `every` or `cron`: mutually exclusive, at least one required. `every` is a duration and also decides when the task first runs; `cron` is a cron expression (for example `"0 * * * *"`) and cron scheduling is based on system time. In the UI the Interval field sets `every`.
- `offset`: a duration that delays execution but preserves the original time range; time ranges in the task stay relative to the specified execution time. Use it to allow for late-arriving data.

Scheduling rule: a task saved at 2:30 with `every: 1h` first runs at 3:00 and every hour after that.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 "Task options" page, article body (lines 574-626) read from the downloaded text.

Removed: the statement that the UI injects the `option task` block and the `range(start: -task.every)` suggestion, which the page does not state.
