---
id: computing-software.database-administration.sqlite.controlling-the-query-planner
name: controlling-the-query-planner
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-query-planner, indexed-by, cross-join-hint, likelihood, not-indexed, unary-plus]
level: advanced
status: verified
description: "Steer the SQLite query planner when it picks badly: CROSS JOIN to fix join order, INDEXED BY / NOT INDEXED, unary + to disqualify an index, likelihood(), and stat data."
sources:
  - https://www.sqlite.org/optoverview.html#manual_control_of_query_plans_using_cross_join
  - https://www.sqlite.org/lang_indexedby.html
  - https://www.sqlite.org/lang_corefunc.html#likelihood
  - https://www.sqlite.org/queryplanner-ng.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controlling the SQLite query planner

First try the non-invasive fix: run `ANALYZE` (or `PRAGMA optimize`) so the planner has
`sqlite_stat1` (and stat4) data. Most bad plans come from missing statistics. Only then use
the manual controls below. sqlite.org/queryplanner-ng.html (2024 update) says the planner has improved so much you should never need these hacks, they remain only for compatibility, and suboptimal plans should be reported on the SQLite Forum.

## Force join order with CROSS JOIN
SQLite treats `CROSS JOIN` as a request to keep the left table as the outer loop:
```sql
SELECT ... FROM small_filter_table AS f CROSS JOIN big_table AS b ON b.key = f.key WHERE f.flag = 1;
```
Plain `JOIN`/`INNER JOIN`/`NATURAL JOIN`/comma joins may be reordered; only the keyword `CROSS` disables reordering (optoverview 7.1.2).

## INDEXED BY / NOT INDEXED
```sql
SELECT * FROM orders INDEXED BY orders_customer_created WHERE customer_id = ? ORDER BY created_at;
SELECT * FROM orders NOT INDEXED WHERE status = 'open';     -- force a full scan
```
INDEXED BY is an assertion, but a weak one: on 3.50.4 a plain index not matching the WHERE clause still gave `SCAN orders USING INDEX o_status` (no error). A partial index whose condition the query does not imply failed with `no query solution`, and a missing index fails with `no such index`. Brittle if the index is renamed or dropped.

## Disqualify a term from index use
Prefix a column with unary `+` to stop that term constraining an index (the docs call it a last-resort workaround). It also strips type affinity, so `+x=5` can change the result of the comparison:
```sql
SELECT * FROM t WHERE +status = 'open' AND created_at > ?;    -- prefers an index on created_at
```

## likelihood() / unlikely() / likely()
Hint that WHERE terms are probably not true (the docs: SQLite otherwise assumes unindexed terms are likely true). `likelihood(X, p)` needs a constant p between 0.0 and 1.0 (checked: other values raise an error):
```sql
SELECT * FROM events WHERE unlikely(is_error = 1) AND device_id = ?;
SELECT * FROM t WHERE likelihood(json_extract(data, '$.vip') = 1, 0.01);
```

## Stat tables you can edit
Per queryplanner-ng, for new databases run `ANALYZE sqlite_schema` to create `sqlite_stat1`, then pre-populate it with ordinary INSERTs describing a typical database. The Query Planner Stability Guarantee (same plan while schema, ANALYZE state and SQLite version are unchanged) is disabled by default: enable with `SQLITE_ENABLE_QPSG` or `SQLITE_DBCONFIG_ENABLE_QPSG`.

## Diagnose
```sql
EXPLAIN QUERY PLAN SELECT ...;       -- SCAN vs SEARCH ... USING INDEX, temp b-tree for ORDER BY
.expert                              -- CLI: index suggestions
```

## Verify
`EXPLAIN QUERY PLAN` shows the intended join order and `SEARCH ... USING INDEX` lines, and
timings improve on realistic data volumes.
