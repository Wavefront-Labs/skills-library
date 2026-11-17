---
id: computing-software.database-administration.postgresql.wal-archiver-monitoring
name: wal-archiver-monitoring
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-stat-archiver, wal-archiving, archive-command, failed-count, monitoring, alerting]
level: practitioner
status: docs-checked
description: "Monitor PostgreSQL WAL archiving with pg_stat_archiver and .ready files, alert on failures and lag, and unstick a failing archive_command safely."
sources:
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ARCHIVER-VIEW
  - https://www.postgresql.org/docs/current/continuous-archiving.html
  - https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-ARCHIVE-COMMAND
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAL archiver monitoring

A broken archive means no point-in-time recovery past the break, and WAL cannot be recycled until archiving succeeds. Monitor it like an outage.

## The view
```sql
SELECT archived_count, last_archived_wal, last_archived_time,
       failed_count, last_failed_wal, last_failed_time,
       now() - last_archived_time AS since_last_ok, stats_reset
FROM pg_stat_archiver;
```
Failing state: `last_failed_time > last_archived_time`. The view always has a single row.

Files are normally archived oldest to newest, but not guaranteed (promotion, crash recovery), so do not assume that everything older than `last_archived_wal` is archived.

## Alert rules
| Alert | Condition |
|---|---|
| archiving failing | `last_failed_time > last_archived_time`, sustained for a window you choose |
| archiving stalled | `now() - last_archived_time` well above your `archive_timeout` (idle systems also look stalled) |
| failures rising | increase of `failed_count` over a window |

Pick thresholds for your own WAL volume and disk headroom.

## Unsticking
1. Read the server log for the archive command's error output.
2. Typical causes: destination full, credentials expired, permissions, the destination file already exists (a good archive command refuses to overwrite and returns nonzero).
3. Fix the cause. A nonzero exit status makes PostgreSQL retry periodically until it succeeds; check `archived_count` rising.
4. Never delete files from pg_wal by hand to free space; add space first.
5. If the archive truly must be abandoned, take a **new base backup** immediately: PITR cannot cross the gap.

## Gotchas
- `failed_count` is cumulative; alert on recent failures, not the counter value.
- The archive command must return zero if and only if it succeeded. If it is killed by a signal (other than SIGTERM) or the shell exits with status above 125 (such as command not found), the archiver aborts and restarts and the failure is not reported in `pg_stat_archiver`; watch the server log too.
- A command that exits 0 but writes to the wrong place looks healthy here; verify restores with your backup tool.

## Checked

2026-10-31. Confirmed against the PostgreSQL pg_stat_archiver view documentation (columns, single row, ordering caveat) and the continuous archiving page (zero exit status if and only if success, nonzero means retry, refuse to overwrite, signal and status above 125 not reported in the view). Removed unconfirmed: `.ready` file counting and `pg_ls_archive_statusdir()`, 16 MB segment sizing, numeric alert thresholds, the 3-failure retry interval, the `/bin/true` workaround, `archive_mode = always` on standbys, specific log message text, backup-tool check commands.

Method: documentation only; no commands were run.
