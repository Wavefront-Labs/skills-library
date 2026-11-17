---
id: computing-software.database-administration.sqlite.explain-query-plan
name: explain-query-plan
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-query-planner, explain-query-plan, scan-vs-search, covering-index, temp-b-tree, automatic-index, eqp]
level: practitioner
status: verified
description: "Read SQLite EXPLAIN QUERY PLAN output (SCAN vs SEARCH, covering index, temp b-tree, automatic index) and fix slow queries with the right index."
sources:
  - https://sqlite.org/eqp.html
  - https://sqlite.org/queryplanner.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EXPLAIN QUERY PLAN

**Goal:** see in seconds whether a SQLite query uses an index and what to add if not.

## Run it
```sql
EXPLAIN QUERY PLAN
SELECT id, total FROM orders WHERE customer_id = 42 ORDER BY created_at DESC LIMIT 20;
```
Run it from any client (tested with Python sqlite3 on 3.50.4; the plan text is in the `detail` column).

## Read it
| Line | Meaning |
|---|---|
| `SCAN orders` | Full table scan (bad on big tables, fine on tiny ones) |
| `SEARCH orders USING INDEX idx_orders_customer (customer_id=?)` | Index lookup on the listed columns |
| `SEARCH ... USING COVERING INDEX ...` | Answered from the index alone, no table access (seen after adding `total` as a third index column) |
| `SEARCH ... USING INTEGER PRIMARY KEY (rowid=?)` | rowid lookup (fastest) |
| `USE TEMP B-TREE FOR ORDER BY` | Sort step: index did not provide the order |
| `USE TEMP B-TREE FOR DISTINCT/GROUP BY` | Temporary structure for grouping |
| `SEARCH ... USING AUTOMATIC COVERING INDEX (col=?)` | SQLite built a throwaway index for this join: you probably need a permanent one |
| `BLOOM FILTER ON ...` | Join pre-filter (seen on 3.50.4 alongside an automatic index) |
| `CORRELATED SCALAR SUBQUERY` | Subquery re-run per row |
Indentation shows nesting; for joins, the outer loop is listed first.

## Fix pattern
For the example, one index serves filter and order:
```sql
CREATE INDEX idx_orders_customer_created ON orders(customer_id, created_at);
```
Plan becomes `SEARCH orders USING INDEX idx_orders_customer_created (customer_id=?)`
with no TEMP B-TREE. Add `total` as a trailing column to make it covering.

## Gotchas
- SQLite uses at most one index per table per query, except the OR optimisation (`MULTI-INDEX OR`, seen for `a=1 OR b=2` with separate indexes); for `a=1 AND b=2` only one index was used. A composite index beats two single-column ones.
- Functions on columns (`WHERE lower(email)=?`) need an expression index on the same expression.
- `LIKE 'abc%'` (literal prefix) is optimised only if the column is indexed with NOCASE (default case-insensitive LIKE) or BINARY when `PRAGMA case_sensitive_like=ON` (optoverview; reproduced: BINARY index gave `SCAN`, NOCASE index gave a range `SEARCH`).
- Without `ANALYZE` stats, the planner guesses; plans can change after ANALYZE / `PRAGMA optimize`.
- Plain `EXPLAIN` (without QUERY PLAN) shows VDBE bytecode, rarely what you want.

## Verify
Plan shows SEARCH with the intended index and no AUTOMATIC INDEX or TEMP B-TREE;
measure query time before and after.
