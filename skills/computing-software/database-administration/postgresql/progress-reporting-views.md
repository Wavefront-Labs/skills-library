---
id: computing-software.database-administration.postgresql.progress-reporting-views
name: progress-reporting-views
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-monitoring, pg-stat-progress, pg-stat-progress-vacuum, pg-stat-progress-create-index, pg-stat-progress-copy, pg-stat-progress-basebackup, long-running-maintenance]
level: practitioner
status: verified
description: "Track how far a running VACUUM, CREATE INDEX, CLUSTER, ANALYZE, COPY or pg_basebackup has got with the pg_stat_progress_* views, and estimate time remaining."
sources:
  - https://www.postgresql.org/docs/current/progress-reporting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Progress reporting views (pg_stat_progress_*)

**Goal:** know whether a long maintenance operation is moving, which phase it is in, and roughly when it ends.

## Available views
| View | Covers |
|---|---|
| `pg_stat_progress_vacuum` | VACUUM and autovacuum (not VACUUM FULL) |
| `pg_stat_progress_cluster` | CLUSTER and VACUUM FULL |
| `pg_stat_progress_create_index` | CREATE INDEX / REINDEX (incl. CONCURRENTLY) |
| `pg_stat_progress_analyze` | ANALYZE |
| `pg_stat_progress_copy` | COPY FROM/TO (14+) |
| `pg_stat_progress_basebackup` | pg_basebackup on the sending server |

## VACUUM percentage
```sql
SELECT p.pid, p.relid::regclass, p.phase,
       round(100.0 * p.heap_blks_scanned / nullif(p.heap_blks_total,0), 1) AS scanned_pct,
       round(100.0 * p.heap_blks_vacuumed / nullif(p.heap_blks_total,0), 1) AS vacuumed_pct,
       p.index_vacuum_count, now() - a.xact_start AS running_for
FROM pg_stat_progress_vacuum p JOIN pg_stat_activity a USING (pid);
```
`index_vacuum_count > 1` means the dead-TID memory filled and indexes were scanned again: raise `maintenance_work_mem` / `autovacuum_work_mem` (17+ uses a far more compact TID store).

## CREATE INDEX
```sql
SELECT pid, relid::regclass, index_relid::regclass, phase,
       blocks_done, blocks_total, tuples_done, tuples_total,
       lockers_done, lockers_total
FROM pg_stat_progress_create_index;
```
For `CONCURRENTLY`, a phase of `waiting for old snapshots` with `lockers_total > 0` means an old transaction is blocking completion; find it with `current_locker_pid` and `pg_stat_activity`.

## COPY and base backups
```sql
SELECT relid::regclass, command, type, bytes_processed, bytes_total, tuples_processed FROM pg_stat_progress_copy;
SELECT pid, phase, pg_size_pretty(backup_streamed) streamed, pg_size_pretty(backup_total) total FROM pg_stat_progress_basebackup;
```
`bytes_total` is 0 when reading from a pipe/STDIN; `backup_total` is NULL if `--no-estimate-size` was used.

## Estimating ETA
Sample twice N seconds apart, divide remaining blocks by blocks/second. Phases are not linear (vacuuming indexes can dwarf the heap scan), so estimate per phase.

## Gotchas
- Rows only exist while the command runs; an empty result means it finished or never started.
- Autovacuum workers appear in `pg_stat_progress_vacuum` too (docs); identify them with `pg_stat_activity.backend_type = 'autovacuum worker'`.

## Verify
Run `VACUUM (VERBOSE) big_table` in one session and watch the percentage climb in another.

## Checked
- PostgreSQL 18.6: the view list exists (`pg_stat_progress_analyze`, `_basebackup`, `_cluster`, `_copy`, `_create_index`, `_vacuum`) with the columns used in the skill (`heap_blks_scanned`, `heap_blks_total`, `heap_blks_vacuumed`, `index_vacuum_count`, `lockers_total`, `lockers_done`, `current_locker_pid`, `bytes_total`, `backup_streamed`, `backup_total`; 18 also has `max_dead_tuple_bytes`, `dead_tuple_bytes`, `num_dead_item_ids`). While a `CREATE INDEX` on a 3M-row table ran, the poll showed `building index: scanning table` (`blocks_done` 368 of 28066) then `building index: loading tuples in tree` (1585082 of 2000000 tuples); during `VACUUM (VERBOSE)` with `maintenance_work_mem = 1MB` the VACUUM percentage query returned `scanning heap | 43.5 | 0` and the VACUUM reported `index scans: 0` (the PG17 compact TID store).
- Docs (progress-reporting, app-pgbasebackup, release notes 14 and 17): `pg_stat_progress_copy` added in 14; VACUUM FULL is reported in the cluster view; `waiting for old snapshots` phase and its `lockers_*` columns; `bytes_total` is 0 when unavailable; `backup_total` is always NULL with `--no-estimate-size`; PG17 vacuum memory rewrite.
