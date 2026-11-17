---
id: computing-software.database-administration.postgresql.server-configuration-and-autovacuum
name: server-configuration-and-autovacuum
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgresql-conf, shared-buffers, work-mem, maintenance-work-mem, effective-cache-size, max-wal-size, checkpoint-timeout, checkpoint-completion-target, random-page-cost, pg-stat-statements, autovacuum, vacuum, analyze, bloat, xid-wraparound, transaction-id-wraparound, autovacuum-vacuum-scale-factor, pg-stat-user-tables, pgtune, alter-system, performance-tuning, dead-tuples, freeze]
level: advanced
status: docs-checked
description: "Tune postgresql.conf memory, WAL and checkpoints with starting numbers, find slow SQL via pg_stat_statements, and tune autovacuum per table to control bloat and XID wraparound."
sources:
  - https://www.postgresql.org/docs/current/runtime-config-resource.html
  - https://www.postgresql.org/docs/current/runtime-config-wal.html
  - https://www.postgresql.org/docs/current/routine-vacuuming.html
  - https://www.postgresql.org/docs/current/pgstatstatements.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostgreSQL server configuration and autovacuum — sane settings, then per-table tuning

**Goal:** move a stock PostgreSQL install to settings that match its hardware, find
the queries that actually cost time, and keep autovacuum ahead of bloat and
transaction ID wraparound.

## 1. Starting numbers for a dedicated server
Set with `ALTER SYSTEM SET ...` (writes `postgresql.auto.conf`) or in `postgresql.conf`.
Check whether a reload is enough: `SELECT name, context FROM pg_settings WHERE name = '...'`
(`postmaster` = restart required).

| Parameter | Starting point | Notes |
|---|---|---|
| `shared_buffers` | 25% of RAM (the docs' starting suggestion for a dedicated server) | restart; the OS page cache does the rest |
| `effective_cache_size` | 50–75% of RAM | planner hint only, allocates nothing |
| `work_mem` | 16–64 MB | per sort/hash node, per query, per parallel worker: 200 connections × several nodes can OOM |
| `maintenance_work_mem` | 512 MB–2 GB | VACUUM, CREATE INDEX; autovacuum may allocate up to `autovacuum_max_workers` times this, so cap it with `autovacuum_work_mem` |
| `max_wal_size` | 4–16 GB | too small forces checkpoints by WAL volume |
| `checkpoint_timeout` | 15 min | longer = less WAL (fewer full-page writes), slower crash recovery |
| `checkpoint_completion_target` | 0.9 | the documented default |
| `random_page_cost` | 1.1 on SSD/NVMe | docs: lower suits cached data and fast storage, higher suits magnetic disks |
| `effective_io_concurrency` | 200 on SSD | |
| `wal_compression` | `lz4` or `zstd` if built in (`--with-lz4` / `--with-zstd`) | cuts full-page-write volume |

Raise `work_mem` per session for a known heavy report (`SET work_mem = '256MB'`)
rather than globally. Keep `max_connections` low (100–300) and put PgBouncer in front;
each backend costs memory and contention.

Check checkpoints are timed, not forced: in `pg_stat_checkpointer` (`num_timed`, `num_requested`) or
`pg_stat_bgwriter` (older), `num_requested`/`checkpoints_req` should be small next to
the timed count. Turn on `log_checkpoints = on`.

## 2. Find the expensive queries
```sql
-- postgresql.conf: shared_preload_libraries = 'pg_stat_statements'  (restart)
CREATE EXTENSION pg_stat_statements;
SELECT queryid, calls, round(total_exec_time) AS total_ms,
       round(mean_exec_time::numeric,2) AS mean_ms, rows,
       shared_blks_read, left(query, 80)
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 20;
```
Sort by `total_exec_time` (aggregate load) first, then by `mean_exec_time` (user-facing
latency). Reset after a change with `SELECT pg_stat_statements_reset();`. Also set
`log_min_duration_statement = '500ms'` and consider `auto_explain` for plans of slow
statements.

## 3. Autovacuum: why it falls behind
Every UPDATE/DELETE leaves dead tuples. Autovacuum triggers when dead tuples exceed
`autovacuum_vacuum_threshold + autovacuum_vacuum_scale_factor × reltuples` (defaults
50 + 20%). On a 500M-row table that is 100M dead rows before anything happens.

Global changes worth making on busy systems:
```
autovacuum_max_workers = 5            # default 3; see autovacuum_worker_slots (server start) in the current docs
autovacuum_vacuum_cost_limit = 2000   # default effectively 200 shared by all workers
autovacuum_vacuum_cost_delay = 2ms    # documented default is 2 ms
autovacuum_naptime = 15s
```
Per large or hot table, switch to fixed thresholds:
```sql
ALTER TABLE orders SET (autovacuum_vacuum_scale_factor = 0,
  autovacuum_vacuum_threshold = 100000,
  autovacuum_analyze_scale_factor = 0.01,
  autovacuum_vacuum_insert_scale_factor = 0.05);
```
Find laggards:
```sql
SELECT relname, n_live_tup, n_dead_tup, last_autovacuum, last_autoanalyze, autovacuum_count
FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 20;
```
Watch running vacuums in `pg_stat_progress_vacuum`.

## 4. Things that silently block vacuum
- **Long transactions** and `idle in transaction` sessions hold back the xmin horizon:
  check `pg_stat_activity` for old `xact_start`; set
  `idle_in_transaction_session_timeout = '5min'`.
- **Abandoned replication slots** (`pg_replication_slots` with `active = false`) pin
  both WAL and xmin. Set `max_slot_wal_keep_size`.
- **Hot standby feedback** from replicas running long queries.
- Stale prepared transactions (`pg_prepared_xacts`).

## 5. Transaction ID wraparound
XIDs are 32-bit; tables must be frozen before age reaches ~2 billion or the server
stops accepting writes. Monitor:
```sql
SELECT datname, age(datfrozenxid) FROM pg_database ORDER BY 2 DESC;
SELECT relname, age(relfrozenxid) FROM pg_class WHERE relkind='r' ORDER BY 2 DESC LIMIT 10;
```
Alert at ~500M; aggressive anti-wraparound autovacuum starts at
`autovacuum_freeze_max_age` (200M default). An anti-wraparound vacuum cannot be
cancelled by lock conflicts, so a "stuck" DDL behind one is expected. If close to the
limit, run a manual `VACUUM (FREEZE, VERBOSE)` on the oldest tables, after removing
whatever holds back xmin.

## 6. Bloat
Estimate with the `pgstattuple` extension (`pgstattuple_approx('t')`). Plain VACUUM
makes space reusable but rarely shrinks files; `VACUUM FULL` takes an ACCESS EXCLUSIVE
lock. Use `pg_repack` or `REINDEX INDEX CONCURRENTLY` for online rebuilds. Lower
`fillfactor` (e.g. 80–90) on update-heavy tables to enable HOT updates.

## Verify
- [ ] `SHOW shared_buffers; SHOW work_mem;` return the intended values after restart.
- [ ] `pg_stat_statements` is loaded and the top-20 list is reviewed.
- [ ] Requested checkpoints are a small fraction of timed ones.
- [ ] No table in `pg_stat_user_tables` has dead tuples far above its threshold.
- [ ] Max `age(datfrozenxid)` is under your alert level and trending down after vacuums.
- [ ] No inactive replication slots or hours-old idle-in-transaction sessions.

## Checked
2026-10-31. Confirmed against the PostgreSQL current docs (runtime-config-resource, runtime-config-wal, runtime-config-autovacuum, pgstatstatements source, monitoring-stats, pgstattuple, sql-vacuum, sql-reindex): shared_buffers 25% suggestion, checkpoint_completion_target 0.9, max_wal_size default 1 GB context, wal_compression methods, autovacuum defaults (threshold 50, scale factor 0.2, naptime, cost delay 2 ms, cost limit 200, max workers 3, freeze_max_age 200 million), pg_stat_statements column names, pg_stat_checkpointer num_timed/num_requested. Removed: version-gate claims (14, 15, 13, 12, 17+) and the shared_buffers cap and random_page_cost default that were not readable in the docs. The remaining sizing numbers (work_mem, effective_cache_size, max_wal_size ranges, SSD values) are tuning judgement, not documented figures.
Method: documentation only; no commands were run.
