---
id: computing-software.data-engineering.apache-airflow.timetables-and-cron-schedules
name: timetables-and-cron-schedules
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, timetables, cron-schedule, crondataintervaltimetable, crontriggertimetable, deltadataintervaltimetable, eventstimetable, multiplecrontriggertimetable, schedule-presets, custom-timetable]
level: advanced
status: docs-checked
description: "Pick Airflow schedules: cron presets, CronTriggerTimetable vs CronDataIntervalTimetable (Airflow 3 default change), delta/events timetables, and custom timetables."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/timetable.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/dag-run.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/howto/timetable.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/config_templates/config.yml
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/cli/cli_config.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timetables and cron schedules

**Goal:** DAG runs fire when you expect, with data intervals that match what each run should process.

## Two cron semantics
| Timetable | Run fires | `data_interval` |
|---|---|---|
| `CronDataIntervalTimetable` | At the **end** of the interval: `@daily` run for Oct 15 starts at Oct 16 00:00 | Oct 15 00:00 -> Oct 16 00:00 |
| `CronTriggerTimetable` | **At** the cron time | Zero-length by default (or `interval=timedelta(days=1)` to look back) |
In Airflow 3 a bare cron string such as `@daily` resolves to **`CronTriggerTimetable`** by default (`[scheduler] create_cron_data_intervals=False`); set it to `True` or pass `CronDataIntervalTimetable` for contiguous windows. A DAG that relies on `data_interval_start` to pick "yesterday" needs an explicit data-interval timetable. Be explicit:
```python
from datetime import timedelta
from airflow.sdk import CronDataIntervalTimetable, CronTriggerTimetable
import pendulum
@dag(schedule=CronDataIntervalTimetable("0 2 * * *", timezone="UTC"), start_date=pendulum.datetime(2026, 1, 1, tz="UTC"))
# or
@dag(schedule=CronTriggerTimetable("0 2 * * *", timezone="Europe/London", interval=timedelta(days=1)))
```

## Other built-ins
- `DeltaDataIntervalTimetable(timedelta(hours=6))`: contiguous data intervals at a fixed spacing.
- `DeltaTriggerTimetable(timedelta(days=7))`: fixed spacing, run at a point in time. A bare `timedelta` in `schedule=` resolves to this in Airflow 3 (`[scheduler] create_delta_data_intervals` is documented as not currently consulted; timedelta schedules follow `create_cron_data_intervals`).
- `MultipleCronTriggerTimetable("0 6 * * 1-5", "0 9 * * 6,0", timezone="UTC")`: several crons in one DAG.
- `EventsTimetable(event_dates=[...])`: explicit list of run times (e.g. earnings dates).
- `None` (manual/API only), `"@once"`, `"@continuous"` (run as soon as the previous run finishes).
- Asset-based schedules, including `AssetOrTimeSchedule` and `AssetAndTimeSchedule` combined with a timetable.
## Custom timetable
Subclass `Timetable`, implement `next_dagrun_info(last_automated_data_interval, restriction)` and `infer_manual_data_interval(run_after)`, register it through an `AirflowPlugin` (`timetables = [MyTimetable]`). Use for business calendars (trading days, "last business day of month"). `next_dagrun_info` receives the previous automated run's data interval and a `restriction` (earliest, latest, catchup) and returns a `DagRunInfo` or `None`.

## Gotchas
- By default (`catchup=False`, `[scheduler] catchup_by_default`) missed scheduled times since `start_date` are not backfilled; with `catchup=True` the scheduler creates a run for each scheduled time that has not been run.
- Cron is evaluated in the DAG's time zone; see the time-zone skill for DST behaviour.
- For a data-interval timetable `start_date` is also the start of the first data interval, so the first run does not execute until one schedule period after it.

## Verify
- [ ] `airflow dags next-execution <dag_id> -n 5` shows the expected next logical datetimes.
- [ ] Task logic logs `data_interval_start/end` and they match the intended window.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: the two cron timetable semantics and zero-width versus contiguous data intervals, the Airflow 3 default of `CronTriggerTimetable` and `create_cron_data_intervals=False`, the bare timedelta default, the `airflow.sdk` exports, `interval=` on trigger timetables, EventsTimetable, `@continuous`, the custom timetable methods and plugin registration, `catchup` defaults and `airflow dags next-execution -n` (CLI source). Removed the Airflow 2 default statement, the 2.10 and 3.0 version tags, the `max_active_runs` condition on `@continuous`, the performance remark and the run-id remark, which are not documented.

Method: documentation only; no commands were run.
