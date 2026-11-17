---
id: computing-software.database-administration.mysql.optimizer-trace
name: optimizer-trace
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-optimization, optimizer-trace, explain, index-choice, cost-model, query-tuning]
level: advanced
status: docs-checked
description: "Capture the MySQL optimizer trace as JSON in INFORMATION_SCHEMA.OPTIMIZER_TRACE to see why a plan was chosen, with size, privilege and multi-statement controls."
sources:
  - https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_OPT_TRACE.html
  - https://dev.mysql.com/doc/refman/8.4/en/information-schema-optimizer-trace-table.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optimizer trace

EXPLAIN shows **what** plan was chosen; the optimizer trace is JSON output aimed at explaining
the decisions the optimizer took.

## Capture
```sql
SET SESSION optimizer_trace = 'enabled=on';
SET optimizer_trace_max_mem_size = 1048576;     -- 1048576 is the default; raise it if traces truncate
SELECT * FROM orders WHERE customer_id = 42 AND status = 'open' ORDER BY created_at LIMIT 20;
SELECT QUERY, TRACE, MISSING_BYTES_BEYOND_MAX_MEM_SIZE, INSUFFICIENT_PRIVILEGES
FROM information_schema.OPTIMIZER_TRACE\G
SET SESSION optimizer_trace = 'enabled=off';
```
- `SELECT` and `EXPLAIN SELECT` produce the same trace, so you can trace `EXPLAIN SELECT ...`
  without running an expensive query (subqueries are the exception: SELECT may stop after the first
  subquery, EXPLAIN analyzes all of them). `INSERT`, `REPLACE`, `UPDATE`, `DELETE`, `CALL` and
  others are traced too.
- By default each new trace overwrites the previous one. For stored routines and other
  multi-statement cases use `SET optimizer_trace_offset=<OFFSET>, optimizer_trace_limit=<LIMIT>`:
  a negative offset counts from the newest trace (`-1` with limit `1` is the default: the last one).
  Setting them clears remembered traces and limits memory and overhead; this is better than
  `LIMIT`/`OFFSET` in the `SELECT`.
- `optimizer_trace_features` (for example `greedy_search=off`) turns off tracing of individual
  optimizer features; disabled parts appear as `...`.
- If `MISSING_BYTES_BEYOND_MAX_MEM_SIZE` is nonzero the trace is incomplete: the memory limit was hit.

## Gotchas
- Tracing costs performance; do not leave it on.
- If a traced query uses views or stored routines with `SQL SECURITY DEFINER` and you are not allowed
  to see their bodies, the trace is empty and `INSUFFICIENT_PRIVILEGES` is 1.
- Tracing can be compiled out of a server build, and the setting is per session.

## Verify
The access path in the trace matches what `EXPLAIN` reports; after your fix (statistics, index,
rewrite) re-capture and compare.

## Checked
2026-11-01. Confirmed against the MySQL server developer page Optimizer Trace (enabling, EXPLAIN SELECT, offset/limit, features, security checks), the 8.4 manual page for the OPTIMIZER_TRACE table (columns, INSUFFICIENT_PRIVILEGES) and the 8.4 server system variables page (optimizer_trace_max_mem_size default 1048576, optimizer_trace_limit). Removed: the walkthrough of JSON section names (join_optimization, range_analysis and so on), tuning rules of thumb, the 8.0.20 hint note, and DUMPFILE advice (not confirmed on those pages).
Method: documentation only; no commands were run.
