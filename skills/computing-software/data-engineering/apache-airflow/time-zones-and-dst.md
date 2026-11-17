---
id: computing-software.data-engineering.apache-airflow.time-zones-and-dst
name: time-zones-and-dst
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, airflow-timezones, pendulum, default-timezone, dst, daylight-saving, timezone-aware-dag, cron-timezone, utc]
level: practitioner
status: docs-checked
description: "Schedule Airflow DAGs in local time correctly: timezone-aware start_date with pendulum, default_timezone, how cron behaves across DST transitions, and UTC storage of dates."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/timezone.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/cron.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time zones and DST in Airflow

**Goal:** "run at 06:00 Sydney time" means 06:00 Sydney time all year, and logs/dates are unambiguous.

## Rules of the system
- Airflow stores datetimes in UTC internally and in the database. The UI shows UTC by default; users can pick another zone in the UI menu (a per-browser setting).
- A DAG's time zone comes from its time-zone-aware `start_date` (use `pendulum`, not the standard library `timezone`); otherwise `[core] default_timezone` applies (`utc` after install; also `system` or an IANA name). Keep that setting identical on all Airflow nodes.
- A naive `start_date` or `end_date` is assumed to be in `default_timezone`; always use aware datetimes.

## Local-time schedule
```python
import pendulum
from airflow.sdk import dag

@dag(schedule="0 6 * * *",
     start_date=pendulum.datetime(2026, 1, 1, tz="Australia/Sydney"),
     catchup=False)
def morning_report(): ...
```
Cron schedules on a time-zone-aware DAG respect daylight saving time, so the run stays at 06:00 local through DST changes (the UTC time shifts by an hour). The docs' example: `0 0 * * *` with a `US/Eastern` start date runs at 04:00 UTC during DST and 05:00 UTC otherwise.

## DST edge cases
- During DST transitions some local datetimes do not exist or are ambiguous; pendulum raises an exception when asked to create one, which is why you should always create aware datetimes.
- `timedelta` and `relativedelta` schedules respect DST for the start date but do not adjust for it for later runs: a DAG starting at `pendulum.datetime(2020, 1, 1, tz="UTC")` with `timedelta(days=1)` runs daily at the same UTC time. Use cron for "same local time daily".
- Keep the timezone library current: the docs warn that pendulum's own timezone database is updated less often than IANA's, and `PYTZDATA_TZDATADIR` can point it at the system database.

## Templates
- Templates receive time-zone-aware datetimes but they are not converted to local time: they remain in UTC. Convert in the DAG, for example `pendulum.timezone("Australia/Sydney").convert(logical_date)`.
- For business-day partitions in local time, compute the local date in the task, not from `ds`.

## Recommendation
The docs recommend authoring DAGs in UTC where possible; use local-zone DAGs only for business-facing deadlines (reports at local opening time).

## Verify
- [ ] The run time in UTC shifts by an hour across the next DST change while the local time stays fixed.
- [ ] Task logs print the local date used for partitioning.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: UTC storage, UI zone selector, `default_timezone`, aware `start_date` with pendulum, naive datetime interpretation, cron respecting DST including the US/Eastern 04:00/05:00 UTC example, `timedelta` schedules not adjusting for DST, templates staying in UTC with explicit conversion, the DST exception remark and the UTC recommendation (timezone.rst). Removed the skipped-hour and repeated-hour behaviour, the 23/25 hour interval claim and the `in_timezone` template call, which the docs do not state.

Method: documentation only; no commands were run.
