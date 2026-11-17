---
id: computing-software.database-administration.mysql.explain-analyze-and-format-tree
name: explain-analyze-and-format-tree
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, mysql-optimization, explain-format-tree, explain-analyze, explain, query-plan, access-type, using-filesort, using-temporary]
level: practitioner
status: verified
description: "Read MySQL 8 query plans with EXPLAIN (traditional columns), FORMAT=TREE and EXPLAIN ANALYZE to find full scans, bad join order and misestimated rows."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/explain.html
  - https://dev.mysql.com/doc/refman/8.4/en/explain-output.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EXPLAIN in MySQL 8

**Goal:** from a slow query to the specific plan step that costs the time.

## Traditional EXPLAIN: columns that matter
```sql
EXPLAIN FORMAT=TRADITIONAL SELECT ... ;
```
The default format is set by `explain_format`: `TRADITIONAL` in 8.4, **`TREE` in 9.7** (per the 9.7 manual; confirmed `@@explain_format = TREE` on 9.7.4), so a bare `EXPLAIN` there prints the tree. Add `FORMAT=TRADITIONAL` (or `SET SESSION explain_format=TRADITIONAL`) to get the columns below.
- `type` (best to worst): `const`/`eq_ref` > `ref` > `range` > `index` (full index scan) > `ALL` (full table scan).
- `key` / `key_len`: which index and how many bytes of it are used (tells you
  how many leading columns of a composite index apply).
- `rows` x `filtered`%: estimated rows passed to the next table.
- `Extra`: `Using index` (covering, good), `Using where`, `Using filesort` and
  `Using temporary` (sort/group not satisfied by an index), `Using join buffer (hash join)`. All of these were reproduced on 9.7.4 (an unindexed join gave `Using where; Using join buffer (hash join)`; `GROUP BY ... ORDER BY` on an unindexed column gave `Using temporary; Using filesort`; a covered `cid = 5` lookup gave `Using index`).

## FORMAT=TREE (8.0.16, experimental then) and EXPLAIN ANALYZE (8.0.18+)
```sql
EXPLAIN FORMAT=TREE SELECT ...;     -- iterator tree, estimates only, nothing executed
EXPLAIN ANALYZE SELECT ...;         -- RUNS the query, adds actuals
```
Sample line:
```
-> Nested loop inner join  (cost=4.95 rows=9) (actual time=0.153..0.427 rows=12 loops=1)
    -> Filter: (o.status = 'open')  (cost=1.15 rows=3) (actual time=0.09..0.11 rows=1200 loops=1)
```
Read inside-out. Compare `rows` (estimate) with actual `rows` x `loops`: a 3 vs
1200 gap means the optimizer chose the join order on a wrong estimate → fix
statistics (ANALYZE TABLE, histograms) or the predicate.
`actual time=first..last` is milliseconds per loop.

## Gotchas
- EXPLAIN ANALYZE executes the statement. The manual lists SELECT, multi-table UPDATE/DELETE and TABLE; a single-table `UPDATE`/`DELETE` printed `<not executable by iterator executor>` on 9.7.4 and an `INSERT` printed only the plan with no `actual` figures. For data-changing statements wrap in a transaction and roll back, or
  test on a copy. `EXPLAIN ANALYZE` cannot be used with `FOR CONNECTION` (manual).
- `FORMAT=JSON` shows cost details and `used_columns`; useful for tooling. The JSON layout changed: `explain_json_format_version` defaults to 2 on 9.7.4 (output carries `"json_schema_version": "2.0"`), so parsers written for the version-1 `query_block` layout need updating or `SET explain_json_format_version=1`.
- `EXPLAIN FOR CONNECTION <id>` shows the plan of a statement running right now.
- MariaDB: `ANALYZE SELECT ...` (and `ANALYZE FORMAT=JSON`) instead of EXPLAIN ANALYZE.
- Plans can differ with real bind values; test with representative literals.

## Verify
After a fix, `EXPLAIN ANALYZE` actual time drops and `type` moved away from
`ALL`/`index` on the big table; slow-log `Rows_examined` for the digest falls.
