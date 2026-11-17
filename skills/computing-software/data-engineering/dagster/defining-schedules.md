---
id: computing-software.data-engineering.dagster.defining-schedules
name: defining-schedules
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, schedule, scheduledefinition, cron-schedule, schedule-decorator, croniter]
level: practitioner
status: docs-checked
description: "Define Dagster schedules with ScheduleDefinition or the @schedule decorator, cron expressions, and logging during evaluation."
sources:
  - https://docs.dagster.io/guides/automate/schedules/defining-schedules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Defining schedules

Goal: run assets or jobs on a cron cadence.

Two forms:
1. `ScheduleDefinition` with a target and `cron_schedule` (docs example runs all assets every day at midnight).
2. The `@schedule` decorator, more flexible than `ScheduleDefinition` (for example, configure job behaviour based on the scheduled run time, or emit log messages):

```python
@schedule(target="*", cron_schedule="0 0 * * *")
def basic_schedule():
    ...
    # things the schedule does, like returning a RunRequest or SkipReason
```

`cron_schedule` accepts standard cron expressions. If your `croniter` dependency is >= 1.0.12 it also accepts `@daily`, `@hourly` and `@monthly`.

## Logging
Log messages emitted in the schedule evaluation function are visible in the UI when you inspect a tick in the schedule's tick history. Gotcha: schedule logs are stored in the instance's compute log storage, so it must be configured to view them.

## Checked
2026-11-08. Confirmed against the Dagster docs page Defining schedules (raw markdown from the docs repo): both forms, the decorator snippet, croniter note, logging note. Nothing removed.
Method: documentation only; no commands were run.
