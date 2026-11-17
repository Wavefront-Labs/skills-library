---
id: computing-software.database-administration.time-series-databases.timescale-user-defined-actions
name: timescale-user-defined-actions
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-jobs, timescale-user-defined-actions, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Schedule your own SQL procedures with the TimescaleDB job scheduler."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User-defined actions

**Goal:** Schedule your own SQL procedures with the TimescaleDB job scheduler.

## Steps
```sql
CREATE PROCEDURE rollup_daily(job_id int, config jsonb) LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO daily SELECT time_bucket('1 day', time), device_id, avg(temp) FROM conditions
  WHERE time >= now() - INTERVAL '2 days' GROUP BY 1,2 ON CONFLICT DO NOTHING;
END $$;
SELECT add_job('rollup_daily', '1 day', initial_start => now());
```
- The action is a function or procedure taking `job_id` and `config`; both are required in the signature. `config` (JSONB) is passed in when it runs.
- `add_job(proc, schedule_interval, config, initial_start, scheduled, check_config, fixed_schedule, timezone)`. By default (`fixed_schedule => true`) runs are aligned to `initial_start`; with `fixed_schedule => false` the next start is the last finish plus the interval. `check_config` validates the config and must be a function, not a procedure.
- Inspect: `SELECT * FROM timescaledb_information.jobs;` and `timescaledb_information.job_stats`.
- Alter: `SELECT alter_job(<id>, scheduled => false);` (also `max_retries`, `retry_period`, `max_runtime`); run now: `CALL run_job(<id>);` (a procedure, so use `CALL`); delete: `SELECT delete_job(<id>);`.
- Make actions idempotent; `max_retries` of -1 means unlimited retries.

**Gotcha:** Background workers are limited by `timescaledb.max_background_workers` and `max_worker_processes`, so many jobs delay each other.

## Verify
- `job_stats.last_run_status` is Success.
- The output table shows the expected rows once per day.

## Checked

Checked 2026-11-03 against the timescale/docs repository: api/jobs-automation/add_job, alter_job, run_job, delete_job, use-timescale/jobs/create-and-manage-jobs, api/informational-views/jobs. Removed: the claim that failed jobs retry by default per `max_retries` (replaced by the documented meaning of the settings).

Method: documentation only; no commands were run.
