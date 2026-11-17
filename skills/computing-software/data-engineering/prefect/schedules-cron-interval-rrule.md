---
id: computing-software.data-engineering.prefect.schedules-cron-interval-rrule
name: schedules-cron-interval-rrule
category: computing-software
field: data-engineering
product: prefect
tags: [schedules, cron, rrule, interval, scheduler-service]
level: practitioner
status: docs-checked
description: "Prefect cron, interval and RRule schedule properties, DST behaviour, the Scheduler service run-creation limits and its settings."
sources:
  - https://docs.prefect.io/v3/concepts/schedules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick a schedule type and know how runs are created.

Three types, all accepting `active` (`false` keeps config but stops new runs).

Cron: `cron` (required), `day_or` (default `True`, cron-compatible OR; `False` ANDs day and weekday), `timezone` (IANA). Parsed with croniter; `R` and `H` expressions are not supported. Example `0 9 * * MON-FRI`.

Interval: `interval` (required; seconds, ISO 8601 such as `PT10M`, or `1:30:00`), `anchor_date` (fixed reference, not a start time; defaults to current UTC), `timezone`. Intervals under 24 hours follow UTC; longer ones follow DST.

RRule: `rrule` (dateutil `rrulestr` syntax), `timezone`. Max length 6,500 characters. `COUNT` is not supported; use `UNTIL`.

```yaml
schedule:
  interval: PT10M
  timezone: America/Chicago
```

The Scheduler service (started by `prefect server start`) only creates `Scheduled` runs, the fewest satisfying: no more than 100 runs, none more than 100 days ahead, at least 3 runs, runs until at least 1 hour ahead. Changing a schedule removes unstarted scheduled runs and recreates them.

Settings (view with `prefect config view --show-defaults`): `PREFECT_SERVER_SERVICES_SCHEDULER_ENABLED` True, `_LOOP_SECONDS` 60.0, `_MIN_RUNS` 3, `_MAX_RUNS` 100, `_MIN_SCHEDULED_TIME` PT1H, `_MAX_SCHEDULED_TIME` P100D, `_DEPLOYMENT_BATCH_SIZE` 100, `_INSERT_BATCH_SIZE` 500.

## Checked

2026-11-09. Confirmed: Schedules page (docs.prefect.io/v3/concepts/schedules): cron, interval and RRule properties, croniter R and H limitation, day_or, DST behaviour, 6,500 character RRule limit, COUNT unsupported, Scheduler run-creation constraints and settings defaults, schedule change behaviour. Nothing removed.

Method: documentation only; no commands were run.
