---
id: computing-software.database-administration.cockroachdb.scheduled-backups
name: scheduled-backups
category: computing-software
field: database-administration
product: cockroachdb
tags: [scheduled-backups, create-schedule-for-backup, recurring, full-backup-always, backup-compaction]
level: practitioner
status: docs-checked
description: "Create and manage CockroachDB backup schedules with CREATE SCHEDULE FOR BACKUP: RECURRING, FULL BACKUP, schedule options, privileges and credentials caveats."
sources:
  - https://www.cockroachlabs.com/docs/stable/create-schedule-for-backup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: automate backups with a cadence the cluster can sustain.

Syntax: `CREATE SCHEDULE [IF NOT EXISTS] <label> FOR BACKUP [targets] INTO '<location>' [WITH <backup_options>] RECURRING <crontab> [FULL BACKUP <crontab|ALWAYS>] [WITH SCHEDULE OPTIONS ...]`. Targets are a cluster, `DATABASE`s or tables; locations are cloud storage or `nodelocal`, with year/month/day subdirectories.

Example that takes only full backups daily:
```sql
CREATE SCHEDULE core_schedule_label
  FOR BACKUP INTO 's3://test/schedule-test-core?AWS_ACCESS_KEY_ID=x&AWS_SECRET_ACCESS_KEY=x'
    RECURRING '@daily'
    FULL BACKUP ALWAYS
    WITH SCHEDULE OPTIONS first_run = 'now';
```
If you omit the `FULL BACKUP` clause, CockroachDB creates a second schedule for fulls; the default full cadence is `@weekly` for incrementals recurring more than 1 hour and up to 1 day.

Schedule options include `first_run`, `on_execution_failure` (`retry`, `reschedule`, `pause`) and `on_previous_running` (`start`, `skip`, `wait`).

Privileges: full cluster backups require the `admin` role; otherwise read access on everything backed up (`CONNECT` for databases, `SELECT` for tables), plus access to the destination.

Gotchas from the page:
- `AS OF SYSTEM TIME` cannot be set on scheduled backups; they run as of the scheduled time.
- Do not schedule faster than backups finish; an incremental waits for the previous incremental from the same schedule.
- Temporary credentials expire; use `implicit` authentication or recreate schedules.
- Setting `backup.compaction.threshold` to `4` (default `0`) enables compaction, a prerequisite for faster restore.

Manage with `SHOW SCHEDULES`, `PAUSE SCHEDULES`, `RESUME SCHEDULES`, `DROP SCHEDULES`, `ALTER BACKUP SCHEDULE`.

Inspect schedules with `SHOW SCHEDULES;`.

## Checked

2026-11-03. Confirmed against the CREATE SCHEDULE FOR BACKUP page (syntax, FULL BACKUP defaults, schedule options, privileges, AS OF SYSTEM TIME, incremental wait, temporary credentials, `backup.compaction.threshold`, PAUSE/RESUME/DROP SCHEDULES). Removed: invented verification outcome (next run time, first job completes).
Method: documentation only; no commands were run.
