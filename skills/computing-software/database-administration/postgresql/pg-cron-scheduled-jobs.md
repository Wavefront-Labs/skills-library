---
id: computing-software.database-administration.postgresql.pg-cron-scheduled-jobs
name: pg-cron-scheduled-jobs
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgres-extensions, create-extension, pg-cron, scheduled-jobs, cron, job-run-details, maintenance-jobs]
level: practitioner
status: docs-checked
description: "Schedule SQL jobs inside PostgreSQL with pg_cron: install, schedule in other databases, read job_run_details, and avoid overlapping runs and history bloat."
sources:
  - https://github.com/citusdata/pg_cron
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pg_cron

**Goal:** routine SQL (partition creation, matview refresh, purges) runs on a
schedule inside the database, visible and logged, without an external cron host.

## Install
```conf
# postgresql.conf (restart)
shared_preload_libraries = 'pg_cron'
cron.database_name = 'postgres'      # the one database that holds the cron schema
cron.timezone = 'UTC'
```
```sql
\c postgres
CREATE EXTENSION pg_cron;
GRANT USAGE ON SCHEMA cron TO ops;    -- non-superusers can schedule jobs as themselves
```

## Schedule
```sql
SELECT cron.schedule('purge-sessions', '*/15 * * * *', $$DELETE FROM sessions WHERE expires_at < now()$$);
-- run in another database (job runs there as the given user)
SELECT cron.schedule_in_database('refresh-mv', '5 * * * *',
  'REFRESH MATERIALIZED VIEW CONCURRENTLY sales_hourly', 'appdb');
SELECT cron.schedule('nightly-vacuum', '30 3 * * *', 'VACUUM (ANALYZE) big_table');
SELECT cron.schedule('heartbeat', '30 seconds', 'SELECT 1');   -- seconds interval (1-59 seconds; not combinable with other units)
SELECT cron.unschedule('purge-sessions');
SELECT cron.alter_job(job_id := 3, active := false);
```

## Observe
```sql
SELECT jobid, jobname, schedule, database, username, active FROM cron.job;
SELECT jobid, status, return_message, start_time, end_time
FROM cron.job_run_details ORDER BY start_time DESC LIMIT 20;
```
Alert on `status = 'failed'`.

## Gotchas
- `job_run_details` grows forever; schedule its own cleanup:
  `DELETE FROM cron.job_run_details WHERE end_time < now() - interval '7 days'`.
- Jobs connect via libpq by default (needs pg_hba entry for localhost);
  set `cron.use_background_workers = on` to use background workers instead (concurrent jobs are then limited by `max_worker_processes`).
- In hot standby mode no jobs run; pg_cron starts automatically when the server is promoted.

## Verify
`cron.job_run_details` shows `succeeded` rows at expected times for each job.

## Checked

2026-10-28. Confirmed against the pg_cron README: shared_preload_libraries, cron.database_name (default postgres), cron.timezone (default GMT), GRANT USAGE ON SCHEMA cron, schedule_in_database, alter_job, seconds intervals (1-59, not combinable), cron.use_background_workers and max_worker_processes, cron.job_run_details, no jobs in hot standby and automatic start on promotion. Removed: the 1.5 version claim, managed-service availability, the overlapping-run claim and the schema-replication claim (not in the README).

Method: documentation only; no commands were run.
