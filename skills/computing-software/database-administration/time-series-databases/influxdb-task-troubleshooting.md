---
id: computing-software.database-administration.time-series-databases.influxdb-task-troubleshooting
name: influxdb-task-troubleshooting
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-tasks, influxdb-task-troubleshooting, influxdb, flux]
level: practitioner
status: docs-checked
description: "Find and fix failing or lagging InfluxDB tasks."
sources:
  - https://docs.influxdata.com/influxdb/v2/process-data/manage-tasks/task-run-history/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/task/run/list/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/task/log/list/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/task/retry-failed/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/task/run/retry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task failure troubleshooting

**Goal:** Find and fix failing or lagging InfluxDB tasks.

## Steps
- `influx task list` then `influx task run list --task-id <id>` shows status, scheduledFor and logs.
- `influx task log list --task-id <id> --run-id <run>` prints the log of a run; read the error there.
- Check the task's token permissions against its source and destination buckets.
- Retry failed runs: `influx task retry-failed --id <task-id>` (optional `--after`, `--before` as RFC3339 times, and `--dry-run` to preview), or one run with `influx task run retry --task-id <id> --run-id <run>`.
- Query concurrency is limited by the `influxd` options `--query-concurrency` and `--query-queue-size`.

**Gotcha:** A task can look active while every run fails; check run logs, not just the task status.

## Verify
- The latest run in `influx task run list --task-id <id>` shows a successful status.
- No growing backlog of unfinished runs.

## Checked

2026-11-03. Confirmed in the task-run-history page and the CLI pages for `task run list`, `task log list`, `task retry-failed` and `task run retry` (flags `--task-id`, `--run-id`, `--id`, `--after`, `--before`, `--dry-run`) and the `influxd` config options page (`query-concurrency`, `query-queue-size`). Removed: the list of typical error causes, the queueing claim and the default values.
Method: documentation only; no commands were run.

