---
id: computing-software.qa-testing-engineering.performance-testing.database-bottleneck-analysis-under-load
name: database-bottleneck-analysis-under-load
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [slow-query-analysis, database-bottlenecks, performance-monitoring, performance-test-environment, pg-stat-statements, explain-analyze, connection-pool, lock-contention]
level: practitioner
status: draft
description: "Find database bottlenecks during load tests: pg_stat_statements and slow logs, EXPLAIN ANALYZE, lock waits, connection pool saturation and index fixes."
sources:
  - https://www.postgresql.org/docs/current/pgstatstatements.html
  - https://www.postgresql.org/docs/current/using-explain.html
  - https://dev.mysql.com/doc/refman/8.0/en/slow-query-log.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Database bottleneck analysis under load

**Goal:** identify which queries and DB resources limit throughput during a performance test.

## Before the test
- PostgreSQL: enable `pg_stat_statements` (`shared_preload_libraries`), then `SELECT pg_stat_statements_reset();` just before the run. Set `log_min_duration_statement = 200` (ms) and `log_lock_waits = on`.
- MySQL: `slow_query_log = 1`, `long_query_time = 0.2`; Performance Schema statement digests.
- SQL Server: Query Store.

## During / after
```sql
SELECT query, calls, round(total_exec_time) AS total_ms, round(mean_exec_time,1) AS mean_ms, rows
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 15;
```
Total time ranks what to fix first (a 2 ms query called 1M times beats a 2 s report query).
- Locks: `SELECT * FROM pg_stat_activity WHERE wait_event_type = 'Lock';` and `pg_locks` joined to activity.
- Connections: active vs max, pool wait time in app metrics (HikariCP `hikaricp_connections_pending`, pgbouncer `SHOW POOLS`).
- Resource: DB CPU, IOPS, buffer cache hit ratio, temp file usage (sorts spilling to disk).

## Diagnose a query
```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT ... ;
```
Look for Seq Scan on large tables, row estimate far from actual (stale stats: `ANALYZE`), nested loops over many rows, sorts spilling to disk.

## Typical findings
Missing index; N+1 queries from the ORM (calls count much higher than requests); pool too small (app threads waiting) or too big (DB thrashing); hot-row lock contention (counters, inventory); long transactions.

## Gotchas
- Test DB with tiny data uses different plans than production; load production-like volumes.
- Caches warm during the test; compare steady state, not the first minutes.

## Verify
After the fix, the top query's total time drops and the load test shows higher throughput at the same latency.
