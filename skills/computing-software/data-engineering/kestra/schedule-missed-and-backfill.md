---
id: computing-software.data-engineering.kestra.schedule-missed-and-backfill
name: schedule-missed-and-backfill
category: computing-software
field: data-engineering
product: kestra
tags: [backfill, recovermissedschedules, schedule, catch-up, triggers-api]
level: advanced
status: docs-checked
description: "Control missed Kestra schedules with recoverMissedSchedules (ALL, LAST, NONE) and replay intervals with backfill from the UI or API."
sources:
  - https://kestra.io/docs/workflow-components/triggers/schedule-trigger
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`recoverMissedSchedules` accepts `ALL` (default), `NONE` or `LAST` (only the last missed schedule per flow).

Global default:

```yaml
kestra:
  plugins:
    configurations:
      - type: io.kestra.plugin.core.trigger.Schedule
        values:
          recoverMissedSchedules: NONE
```

Per trigger: set `recoverMissedSchedules: NONE` in the trigger definition.

Backfill replays schedule intervals between `start` and `end`, including intervals that already succeeded.

- UI: Backfill executions on the flow's Triggers tab; labels can be added.
- Pause and resume are supported; nothing is processed while the trigger is disabled.
- One backfill per trigger; a second returns `409 Conflict`.
- API: `PUT /api/v1/{tenant}/triggers/backfill/create`. `start` is required; `end` defaults to the current time.
- Pause, unpause and delete: `PUT .../backfill/pause`, `PUT .../backfill/unpause`, `POST .../backfill/delete`.
- Deleting a backfill cancels pending catch-up runs only. Deleting the trigger removes its lock, next evaluation date and backfill.

With `NONE`, use backfill to replay a missed window.

## Checked

2026-11-04. Confirmed against "Run Flows on a Cron Schedule with Backfills and Conditions" (triggers/schedule-trigger): recoverMissedSchedules values and ALL default, global and per-trigger config, backfill UI, pause and resume, disabled trigger behaviour, 409 on second backfill, API paths, start required and end defaulting to now, delete backfill versus delete trigger. No claims removed.
Method: documentation only; no commands were run.
