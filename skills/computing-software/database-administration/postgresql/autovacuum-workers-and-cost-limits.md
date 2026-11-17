---
id: computing-software.database-administration.postgresql.autovacuum-workers-and-cost-limits
name: autovacuum-workers-and-cost-limits
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, autovacuum-max-workers, autovacuum-vacuum-cost-limit, autovacuum-tuning, vacuum-cost-delay, bloat, autovacuum]
level: practitioner
status: verified
description: "Size autovacuum workers and the cost limit so vacuum keeps up, and diagnose an autovacuum that runs forever or never finishes on a big table."
sources:
  - https://www.postgresql.org/docs/current/runtime-config-autovacuum.html
  - https://www.postgresql.org/docs/current/runtime-config-resource.html#RUNTIME-CONFIG-RESOURCE-VACUUM-COST
  - https://www.postgresql.org/docs/current/progress-reporting.html#VACUUM-PROGRESS-REPORTING
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autovacuum workers and cost limits

## The budget model
All running autovacuum workers **share** one I/O budget: `autovacuum_vacuum_cost_limit` (default -1 = `vacuum_cost_limit` = 200) points per `autovacuum_vacuum_cost_delay` (2 ms since PG12). Page hit = 1, miss = 2 (PG14+; was 10), dirtying = 20.
- 200 points / 2 ms ≈ up to ~100k pages/s hit, but only ~5k pages/s dirtied (~40 MB/s) split across all workers.
- Adding workers without raising the limit makes each worker **slower**, not vacuum faster.

## Sensible settings for modern SSD servers
```ini
autovacuum_max_workers = 5              # restart required (before PG18)
autovacuum_vacuum_cost_limit = 2000     # shared by the workers
autovacuum_vacuum_cost_delay = 2ms
autovacuum_naptime = 15s                # with many databases/tables
maintenance_work_mem / autovacuum_work_mem = 1GB   # dead-TID memory; fewer index passes
```
Per table, for the one huge hot table:
```sql
ALTER TABLE events SET (autovacuum_vacuum_cost_limit = 4000, autovacuum_vacuum_cost_delay = 0);
```
Tables with per-table cost settings are excluded from the shared balancing.

## Diagnose "autovacuum never finishes"
```sql
SELECT p.pid, p.relid::regclass, p.phase, p.heap_blks_total, p.heap_blks_scanned, p.heap_blks_vacuumed,
       p.index_vacuum_count, a.wait_event_type, a.wait_event, now()-a.xact_start AS running
FROM pg_stat_progress_vacuum p JOIN pg_stat_activity a USING (pid);
```
| Observation | Cause | Fix |
|---|---|---|
| `wait_event = VacuumDelay` most of the time | cost throttling | raise cost limit / lower delay for that table |
| `index_vacuum_count` > 1 and climbing | dead TIDs overflow memory | raise `autovacuum_work_mem` (capped at 1GB before PG17) |
| restarts from zero repeatedly | something cancels it (lock conflict, DDL, `lock_timeout`) | check log for `canceling autovacuum task`; avoid DDL during runs |
| finishes but dead tuples stay | xmin horizon held back | long transaction, abandoned replication slot, `hot_standby_feedback`, prepared xact |
| all workers busy on big tables, small ones starve | too few workers | more workers + higher shared limit |

Check the horizon blockers:
```sql
SELECT pid, backend_xmin, now()-xact_start, state FROM pg_stat_activity WHERE backend_xmin IS NOT NULL ORDER BY age(backend_xmin) DESC LIMIT 5;
SELECT slot_name, xmin, catalog_xmin, active FROM pg_replication_slots;
SELECT gid, prepared FROM pg_prepared_xacts;
```

## Visibility
```ini
log_autovacuum_min_duration = '10s'     # logs I/O, buffer usage, tuples removed, "tuples ... are dead but not yet removable"
```
"dead but not yet removable" in that log line is the smoking gun for a held-back horizon.

## Gotchas
- An anti-wraparound autovacuum (`to prevent wraparound` in pg_stat_activity) does not yield to lock requests; killing it only makes it restart.
- Manual `VACUUM` is unthrottled (`vacuum_cost_delay = 0`) by default: fast, but can saturate I/O in business hours.

## Checked
- PostgreSQL 17.6: defaults (`autovacuum_vacuum_cost_limit` -1, delay 2 ms, `vacuum_cost_limit` 200, page costs 1/2/20 so 100k points/s is about 5k dirtied pages/s, `autovacuum_max_workers` 3 with `postmaster` context, manual `vacuum_cost_delay` 0); per-table cost reloptions accepted; every diagnostic query runs (the progress view has the columns used); `pg_wait_events` lists `VacuumDelay`; with a held snapshot both `VACUUM VERBOSE` and the autovacuum log (`log_autovacuum_min_duration=0`) report `N are dead but not yet removable`. The 17 release notes describe the new VACUUM memory management, the 18 notes make `autovacuum_max_workers` adjustable without restart, and the routine-vacuuming page says wraparound autovacuums are not interrupted. Lock-cancel restarts were not reproduced.
