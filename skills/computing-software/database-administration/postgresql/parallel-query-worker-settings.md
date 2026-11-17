---
id: computing-software.database-administration.postgresql.parallel-query-worker-settings
name: parallel-query-worker-settings
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgresql-conf, max-parallel-workers, parallel-query, max-worker-processes, performance-tuning]
level: practitioner
status: docs-checked
description: "Size max_worker_processes, max_parallel_workers and per-gather limits so parallel query helps analytics without starving OLTP or logical replication workers."
sources:
  - https://www.postgresql.org/docs/current/runtime-config-resource.html#RUNTIME-CONFIG-RESOURCE-ASYNC-BEHAVIOR
  - https://www.postgresql.org/docs/current/how-parallel-query-works.html
  - https://www.postgresql.org/docs/current/when-can-parallel-query-be-used.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parallel query worker settings

## The three nested pools
```
max_worker_processes            (restart, default 8)  every background worker: parallel, logical rep, extensions
 └─ max_parallel_workers         (default 8)  of those, how many may be parallel workers
     ├─ max_parallel_workers_per_gather      per Gather or Gather Merge node in one query (default 2)
     └─ max_parallel_maintenance_workers     per utility command: B-tree, GIN and BRIN CREATE INDEX, VACUUM without FULL (default 2)
```
A worker is only launched if all levels have room; otherwise the plan runs with fewer workers than planned
(in the worst case the leader runs the part below the Gather node entirely by itself). On a standby,
`max_worker_processes` must be the same or higher than on the primary, otherwise queries are not allowed there.

## Starting point
| Workload | per_gather | max_parallel_workers | max_worker_processes |
|---|---|---|---|
| OLTP, many connections | 0-2 | ~cores/2 | cores + logical rep + extension workers |
| Reporting/DW, few sessions | 4-8 | cores | cores + extras |
```sql
ALTER SYSTEM SET max_worker_processes = 24;          -- restart required
ALTER SYSTEM SET max_parallel_workers = 16;
ALTER SYSTEM SET max_parallel_workers_per_gather = 4;
ALTER SYSTEM SET max_parallel_maintenance_workers = 4;
SELECT pg_reload_conf();
```
Budget `max_worker_processes` explicitly: logical replication workers (`max_logical_replication_workers`, default 4,
taken from the same pool; they include apply, parallel apply and table synchronization workers) and extension background workers
also draw on it. Parallel workers are taken from the `max_worker_processes` pool, limited by `max_parallel_workers`.

## Per-query / per-role control
```sql
ALTER ROLE reporting SET max_parallel_workers_per_gather = 6;
ALTER TABLE big_fact SET (parallel_workers = 8);     -- override the size-based heuristic
SET max_parallel_workers_per_gather = 0;              -- disable for a session
```
Planner thresholds: `min_parallel_table_scan_size` (default 8MB), `min_parallel_index_scan_size`,
`parallel_setup_cost` (default 1000), `parallel_tuple_cost` (default 0.1).

## Why a query is not parallel
- Function marked `PARALLEL UNSAFE` (the default for user-defined functions; most system functions are `PARALLEL SAFE`) anywhere in the query;
  mark safe functions `PARALLEL SAFE`.
- The query writes data or locks rows, at top level or in a CTE. Exceptions: `CREATE TABLE ... AS`, `SELECT INTO`, `CREATE MATERIALIZED VIEW` and `REFRESH MATERIALIZED VIEW` can parallelize the underlying SELECT.
- The query might be suspended: a `DECLARE CURSOR` cursor or a PL/pgSQL `FOR x IN query LOOP` never uses a parallel plan.
- The query runs inside another query that is already parallel (for example SQL issued by a function called from a parallel query).
- Single-user mode, or `max_parallel_workers_per_gather = 0`.
- At execution time: a client sends an Execute message with a non-zero fetch count (libpq cannot, but other clients can); the leader then runs the plan serially. Setting `max_parallel_workers_per_gather = 0` for such sessions avoids suboptimal plans.
- Table too small for the thresholds.

## Gotchas
- Each worker can use its own `work_mem` per sort/hash node: memory = workers x nodes x work_mem.
- Parallelism multiplies CPU per query; on a saturated OLTP box it raises latency for everyone.

## Verify
`EXPLAIN (ANALYZE)` shows `Workers Launched` equal to `Workers Planned`; check
`SELECT count(*) FROM pg_stat_activity WHERE backend_type = 'parallel worker';` under load.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): "How Parallel Query Works" and "When Can Parallel Query Be Used?" (conditions that prevent parallel plans, the CTAS-family exception, cursors and PL/pgSQL loops, PARALLEL UNSAFE default for user functions, nested parallel queries, single-user mode, non-zero fetch count, worker limits and leader fallback), the parameters `max_worker_processes` (default 8, server start, standby rule), `max_parallel_workers` (8), `max_parallel_workers_per_gather` (2), `max_parallel_maintenance_workers` (2; B-tree, GIN, BRIN index builds and VACUUM without FULL), `min_parallel_table_scan_size` (8MB), `parallel_setup_cost` (1000), `parallel_tuple_cost` (0.1), `max_logical_replication_workers` (4), and the `parallel_workers` table storage parameter. Removed the "from PG 11" version gate, the serializable-on-standby condition, the JDBC and `could not register background process` remarks, and the pg_cron and TimescaleDB mentions, which the documentation does not give.
Method: documentation only; no commands were run.
