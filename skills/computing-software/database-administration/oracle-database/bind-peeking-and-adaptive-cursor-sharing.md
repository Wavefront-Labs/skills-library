---
id: computing-software.database-administration.oracle-database.bind-peeking-and-adaptive-cursor-sharing
name: bind-peeking-and-adaptive-cursor-sharing
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, adaptive-cursor-sharing, bind-peeking, bind-sensitive, bind-aware, histograms, cursor-sharing, child-cursors]
level: advanced
status: docs-checked
description: "Diagnose Oracle plan flips from bind peeking on skewed data, and use adaptive cursor sharing, histograms, BIND_AWARE hints or baselines to stabilise them."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/improving-rwp-cursor-sharing.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/histograms.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bind peeking and adaptive cursor sharing

## The problem
At hard parse the optimizer **peeks** at the first bind values and builds a plan for them. If
the column is skewed (`status = 'OPEN'` 0.1% vs `'CLOSED'` 99%), the first caller decides the plan
for everyone: an index plan good for rare values runs for the common value, or vice versa.
Symptom: same SQL_ID, sometimes fast, sometimes slow, often "after the cursor aged out" or after stats gathering.

## Adaptive cursor sharing
A cursor is **bind sensitive** when the optimizer peeked at bind values for an equality or range predicate (typically a skewed column with a histogram); the database then monitors executions. When different bind values give significantly different data access patterns or costs, it becomes **bind aware** and the optimizer chooses a plan per bind value's cardinality estimate; the original cursor is marked not shareable (`IS_SHAREABLE = N`). Bind sensitivity is not used for collection binds (e.g. PL/SQL arrays) or when bind counts exceed internal limits.
```sql
SELECT sql_id, child_number, plan_hash_value, is_bind_sensitive, is_bind_aware, is_shareable, executions,
       buffer_gets/NULLIF(executions,0) gets_per_exec
FROM v$sql WHERE sql_id = '&sql_id';
SELECT * FROM v$sql_cs_histogram WHERE sql_id = '&sql_id';       -- execution counts across a three-bucket history histogram
SELECT * FROM v$sql_cs_selectivity WHERE sql_id = '&sql_id';     -- selectivity ranges per predicate with a bind
SELECT * FROM v$sql_cs_statistics WHERE sql_id = '&sql_id';      -- sampled executions; PEEKED = YES if that bind set built the cursor
```
ACS only reacts after it has observed differing executions.

## What the plan was peeked with
```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR('&sql_id', NULL, 'TYPICAL'));   -- cursor_child_no NULL = see the guide; use 0 for the first child
SELECT name, position, datatype_string, value_string FROM v$sql_bind_capture WHERE sql_id = '&sql_id';
```

## Fixes, least to most invasive
1. **Histograms right**: the `METHOD_OPT` statistics preference (see `DBMS_STATS`) controls whether histograms exist on skewed predicate columns; check the current value with `DBMS_STATS.GET_PREFS('METHOD_OPT')`. A histogram is the usual reason a cursor is bind sensitive but the guide does not make it a requirement.
2. **SQL plan baseline** with the plan(s) that are acceptable for all values; multiple accepted plans can coexist with ACS choosing among them.
3. Literal for the skewed column when the value set is tiny (status codes) and hard-parse cost is acceptable.

## CURSOR_SHARING
`CURSOR_SHARING` is `EXACT` by default; `FORCE` replaces literals with system-generated binds (the guide calls it a rare, temporary measure, not a fix), so bind peeking issues then appear on those statements; `SIMILAR` is deprecated. Per statement, the `CURSOR_SHARING_EXACT` hint overrides it.

## Gotchas
- Purging one cursor to force a re-peek: `EXEC DBMS_SHARED_POOL.PURGE('&address,&hash_value','C');` (address and hash_value from `v$sqlarea`; for a cursor the flag may be any character except P, Q, R, T). It is a one-off relief, not a fix.
- Very many child cursors for one SQL: check why they are not shared (`v$sql_shared_cursor`).

## Verify
`is_bind_aware = Y` or a baseline in use, and per-execution gets are stable across bind values.

## Checked
Date 2026-10-22. Oracle Database 19c SQL Tuning Guide (cursor sharing), PL/SQL Packages Reference (DBMS_XPLAN,
DBMS_SHARED_POOL), Database Reference (V$SQL_BIND_CAPTURE). Confirmed: bind-sensitive and bind-aware definitions, V$SQL_CS_*
views, IS_BIND_SENSITIVE / IS_BIND_AWARE / IS_SHAREABLE, CURSOR_SHARING values and the CURSOR_SHARING_EXACT hint,
V$SQL_BIND_CAPTURE columns, DBMS_SHARED_POOL.PURGE cursor flag rule. Corrected: a histogram is not documented as a
requirement for bind sensitivity. Removed (not found in the documentation): the BIND_AWARE hint SQL patch, the
`+PEEKED_BINDS` DBMS_XPLAN format, the `_optim_peek_user_binds` advice, the "11g+" gate, DBMS_STATS METHOD_OPT default
and example (the DBMS_STATS page was too large to read fully).
Method: documentation only; no commands were run.
