---
id: computing-software.database-administration.influxdb.manage-tasks-with-the-cli-and-retry-runs
name: manage-tasks-with-the-cli-and-retry-runs
category: computing-software
field: database-administration
product: influxdb
tags: [tasks, influx-task, retry, run-history, logs]
level: practitioner
status: docs-checked
description: "Create, update, deactivate, retry and inspect Flux tasks with influx task, and read run logs through the API."
sources:
  - https://docs.influxdata.com/influxdb/v2/process-data/manage-tasks/create-task/
  - https://docs.influxdata.com/influxdb/v2/process-data/manage-tasks/update-task/
  - https://docs.influxdata.com/influxdb/v2/process-data/manage-tasks/run-task/
  - https://docs.influxdata.com/influxdb/v2/process-data/manage-tasks/task-run-history/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

```sh
influx task create -f task.flux
influx task update -i TASK_ID -f task.flux
influx task update -i TASK_ID --status inactive
influx task run list --task-id TASK_ID
influx task run retry --task-id TASK_ID --run-id RUN_ID
influx task retry-failed --id TASK_ID --dry-run
```

`--status inactive` cancels scheduled runs and prevents manual runs; set `active` to resume. `retry` needs the task to have run at least once. `retry-failed` accepts `--id`, `--dry-run`, `--after` and `--before` to select failed runs by time.

To retry a run through the API, POST to `/api/v2/tasks/TASK_ID/runs/RUN_ID/retry`.

Run logs come from the API: `GET /api/v2/tasks/TASK_ID/logs`. InfluxDB does not guarantee a task runs at its scheduled time; the logs show `scheduledFor` and `startedAt`. Execution time does not change the time range the task queries.

## Checked

- Date: 2026-11-04
- Confirmed against: https://docs.influxdata.com/influxdb/v2/process-data/manage-tasks/create-task/, https://docs.influxdata.com/influxdb/v2/process-data/manage-tasks/update-task/, https://docs.influxdata.com/influxdb/v2/process-data/manage-tasks/run-task/, https://docs.influxdata.com/influxdb/v2/process-data/manage-tasks/task-run-history/
- Scope: CLI forms, status semantics, retry and log endpoints, timing note.
- Removed: the unconfirmed `/api/v2/tasks/ID/runs` endpoint and the claim that the CLI cannot show logs.
Method: documentation only; no commands were run.
