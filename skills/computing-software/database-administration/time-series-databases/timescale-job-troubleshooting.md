---
id: computing-software.database-administration.time-series-databases.timescale-job-troubleshooting
name: timescale-job-troubleshooting
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-jobs, timescale-job-troubleshooting, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Diagnose Timescale background jobs that stall or fail."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job troubleshooting

**Goal:** Diagnose Timescale background jobs that stall or fail.

## Steps
- Job status: `SELECT j.job_id, j.proc_name, s.last_run_status, s.last_successful_finish, s.next_start, s.total_failures FROM timescaledb_information.job_stats s JOIN timescaledb_information.jobs j USING (job_id);` (`proc_name` is in `jobs`; the counters are in `job_stats`).
- Errors: `SELECT * FROM timescaledb_information.job_errors ORDER BY finish_time DESC LIMIT 20;` (columns include `sqlerrcode` and `err_message`).
- Workers: the docs say `timescaledb.max_background_workers` should equal the number of databases plus the number of concurrent background workers, and `max_worker_processes` should equal the sum of `timescaledb.max_background_workers` and `max_parallel_workers`. A log line `failed to start a background worker` points here.
- Run a job in the foreground now (useful with a higher log level): `CALL run_job(<job_id>);`.
- Pause a job: `SELECT alter_job(<job_id>, next_start => 'infinity');`; restart it with `next_start => now()`. `alter_job` also sets `max_retries` (-1 retries forever), `retry_period`, `max_runtime` and `scheduled`.
- Check for long transactions holding locks with `pg_locks` and `pg_stat_activity` if a job runs but never finishes.

**Gotcha:** Raising `max_background_workers` without raising `max_worker_processes` does not give you more workers.

## Verify
- The failing job reports Success on its next run.
- `job_errors` stops gaining new rows.

## Checked

Checked 2026-11-03 against the timescale/docs repository: api/informational-views/jobs, job_stats, job_errors, api/jobs-automation/alter_job and run_job, _troubleshooting/self-hosted/background-worker-failed-start, self-hosted/configuration/configuration. Removed: the unverified claim that a long transaction blocks compression and retention, the 'needs a restart' remark, and the `max_background_workers` 'jobs plus margin' wording (replaced by the documented formula). Fixed: the original query selected `proc_name` from `job_stats`, which lacks that column.

Method: documentation only; no commands were run.
