---
id: computing-software.database-administration.postgresql.database-wide-statistics-pg-stat-database
name: database-wide-statistics-pg-stat-database
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, pg-stat-statements, pg-stat-database, cache-hit-ratio, temp-files, deadlocks, monitoring]
level: practitioner
status: verified
description: "Read pg_stat_database for health signals: commit/rollback rates, cache hit ratio, temp file spills, deadlocks, checksum failures and session stats, as rates not totals."
sources:
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-DATABASE-VIEW
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-STATS-FUNCTIONS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database-wide statistics (pg_stat_database)

All counters are **cumulative since `stats_reset`**; monitor deltas per interval.

```sql
SELECT datname, numbackends, xact_commit, xact_rollback,
       blks_read, blks_hit,
       round(100.0 * blks_hit / nullif(blks_hit + blks_read, 0), 2) AS hit_pct,
       temp_files, pg_size_pretty(temp_bytes) AS temp_bytes,
       deadlocks, conflicts, checksum_failures, checksum_last_failure,
       session_time, active_time, idle_in_transaction_time,
       sessions, sessions_abandoned, sessions_fatal, sessions_killed,
       stats_reset
FROM pg_stat_database WHERE datname IS NOT NULL;
```

## What each signal means
| Column | Watch for |
|---|---|
| `xact_rollback / xact_commit` | sudden rise = app errors, serialization failures, timeouts |
| `blks_hit / (hit+read)` | buffer cache hit ratio; a common OLTP target is above 99% (rule of thumb, not from the docs). A drop means the working set outgrew `shared_buffers` (or a big scan ran). `blks_read` may still be served by the OS page cache. |
| `temp_files`, `temp_bytes` | sorts/hashes spilling past `work_mem`; correlate with `log_temp_files = 0` to see which queries |
| `deadlocks` | any non-zero delta deserves a look at the log `deadlock detected` entries |
| `conflicts` | standby queries cancelled due to recovery (detail in `pg_stat_database_conflicts`) |
| `checksum_failures` | **page corruption** read from disk; page alarm, investigate storage immediately (NULL when data checksums are off) |
| `sessions_abandoned` | clients disconnecting without Terminate (crashing pods, network drops) |
| `idle_in_transaction_time` | apps holding transactions open |

## Rate query (two samples)
```sql
CREATE TEMP TABLE s1 AS SELECT now() t, * FROM pg_stat_database;
-- wait 60s
SELECT d.datname,
       (d.xact_commit - s1.xact_commit) / extract(epoch FROM now() - s1.t) AS tps,
       d.temp_files - s1.temp_files AS new_temp_files,
       d.deadlocks - s1.deadlocks AS new_deadlocks
FROM pg_stat_database d JOIN s1 USING (datid);
```

## Gotchas
- Stats are reset after a crash or immediate shutdown (a clean shutdown preserves them);
  `stats_reset` tells you the baseline.
- `pg_stat_reset()` zeroes all statistics counters for the current database (not only this view); avoid
  it in production.
- A low hit ratio during nightly batch is normal; alert on sustained daytime drops.

## Verify
Run a query that sorts more than `work_mem` and see `temp_files` increment for that
database; check numbers against `pg_stat_statements` for the top temp-writing statements.

## Checked
- PostgreSQL 18.6: the full column list query ran (30 columns, including `session_time`, `sessions_*`, `checksum_*`, `parallel_workers_*` new in 18); a sort with `work_mem = 64kB` raised `temp_files` from 0 to 2 after `pg_stat_force_next_flush()`; the two-sample rate query ran. Stats persisted across a clean `pg_ctl stop -m fast` (xact_commit 15 -> 18, `temp_files` kept) and reset after `stop -m immediate` plus restart (2 and 0).
- Docs (monitoring-stats page): `checksum_failures` NULL if checksums disabled; `sessions_abandoned` = terminated because connection to the client was lost; `pg_stat_reset()` resets all counters for the current database; `pg_stat_database_conflicts` exists.
- Removed the postgres_exporter sentence (not run here).
