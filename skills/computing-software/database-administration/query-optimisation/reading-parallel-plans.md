---
id: computing-software.database-administration.query-optimisation.reading-parallel-plans
name: reading-parallel-plans
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, parallel-plan, parallel-query, gather, maxdop, execution-plans]
level: practitioner
status: docs-checked
description: "Read PostgreSQL parallel plans (Gather, Gather Merge, workers planned vs launched, partial/finalize aggregates) and know the SQL Server MAXDOP levels, without starving the server."
sources:
  - https://www.postgresql.org/docs/current/parallel-plans.html
  - https://www.postgresql.org/docs/current/how-parallel-query-works.html
  - https://www.postgresql.org/docs/current/when-can-parallel-query-be-used.html
  - https://www.postgresql.org/docs/current/runtime-config-resource.html
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/configure-the-max-degree-of-parallelism-server-configuration-option
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading parallel plans

## PostgreSQL
- A parallel plan has a `Gather` or `Gather Merge` node with exactly one child: the portion of the plan below it runs in parallel. If the node is not at the top, only the part below it is parallel.
- `Gather Merge` means each process produces sorted tuples and the leader does an order-preserving merge; `Gather` reads in whatever order is convenient and destroys any sort order.
- Aggregation is two-stage: `Partial Aggregate` in each process, then `Finalize Aggregate` on the leader. Queries with many groups relative to input rows look less favourable, and aggregates with DISTINCT or ORDER BY, ordered-set aggregates and GROUPING SETS are not parallelised.
- `EXPLAIN` shows the workers the planner chose. At execution the session asks for that many background workers, but the query can run with fewer workers than planned, or none, because the pool is limited by `max_worker_processes` and `max_parallel_workers`. If it is frequent, raise those or lower `max_parallel_workers_per_gather`.
- The leader also runs the parallel portion, but when workers return many tuples it spends most of its time reading them.

Settings (defaults from the docs): `max_parallel_workers_per_gather` = 2 (0 disables parallel query), `max_parallel_workers` = 8, `max_worker_processes` = 8 (server start only), `min_parallel_table_scan_size` = 8MB, plus `parallel_setup_cost` and `parallel_tuple_cost`. Work limits such as `work_mem` apply per worker, so a query with 4 workers can use up to 5 times the resources of a serial one.

No parallel plan is generated when: `max_parallel_workers_per_gather` is 0; the query writes data or locks rows (including in a CTE), except the SELECT part of `CREATE TABLE ... AS`, `SELECT INTO`, `CREATE MATERIALIZED VIEW`, `REFRESH MATERIALIZED VIEW`; the query may be suspended (a `DECLARE CURSOR`, or a PL/pgSQL `FOR x IN query LOOP`); or it calls a function marked `PARALLEL UNSAFE` (user-defined functions are unsafe by default).

## SQL Server
`MAXDOP` can be set at the server level, as the database-scoped configuration, or per query with the `MAXDOP` query hint (`OPTION (MAXDOP n)`). The limit applies per task, not per query. Microsoft's page gives recommendations by NUMA layout; read it for your core counts rather than guessing a number.

## When parallelism hurts
OLTP servers with many concurrent queries: parallel plans take several processes per query. Keep it for reporting workloads or reduce the per-gather worker limit.

## Verify
Compare elapsed time and CPU with parallelism on and off (`EXPLAIN ANALYZE`); check the workers launched equal those planned under typical load.

## Checked
2026-11-01. Confirmed against PostgreSQL docs (parallel-plans, how-parallel-query-works, when-can-parallel-query-be-used, runtime-config-resource) and Microsoft's MAXDOP page: Gather/Gather Merge behaviour, partial and finalize aggregation and its exclusions, worker limits and defaults, the conditions that block parallel plans, and the MAXDOP levels. Removed: SQL Server exchange operators and wait types, cost threshold figures, the table-level `parallel_workers` option, the SERIALIZABLE remark, MySQL parallel-read claims, and the example plan listing.
Method: documentation only; no commands were run.
