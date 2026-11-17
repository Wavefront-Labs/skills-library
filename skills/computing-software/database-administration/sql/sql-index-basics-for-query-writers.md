---
id: computing-software.database-administration.sql.sql-index-basics-for-query-writers
name: sql-index-basics-for-query-writers
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-indexes, b-tree-index, sargable-predicates, index-selectivity]
level: practitioner
status: docs-checked
description: "Write sargable predicates and know which indexes help joins, filters and sorts."
sources: ["https://www.postgresql.org/docs/current/indexes-types.html", "https://www.postgresql.org/docs/current/indexes-multicolumn.html", "https://www.postgresql.org/docs/current/indexes-ordering.html", "https://www.postgresql.org/docs/current/indexes-expressional.html", "https://www.postgresql.org/docs/current/indexes-partial.html", "https://www.sqlite.org/optoverview.html", "https://www.postgresql.org/docs/current/monitoring-stats.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Indexes for query writers

- PostgreSQL B-tree indexes (the default) handle equality and range comparisons (`< <= = >= >`) and constructs equivalent to them such as `BETWEEN` and `IN`, plus `IS NULL`/`IS NOT NULL`. They serve `LIKE` and `~` only when the pattern is a constant anchored at the start (`col LIKE 'foo%'`, not `'%bar'`), and outside the C locale that needs a special operator class. SQLite similarly lists `column = expression`, ranges, `IN`, `IS NULL` and `LIKE`/`GLOB` patterns as terms an index can use.
- Sargable: keep the indexed column bare on one side, e.g. `created_at >= '2025-01-01'` rather than wrapping it in a function. A query on `lower(col)` can use an index only if the index is on the expression, `CREATE INDEX ... ON t (lower(col))` (PostgreSQL; SQLite also supports indexes on expressions and uses them when the query repeats the same expression).
- Multicolumn B-tree `(a, b)` is most efficient with constraints on the leading column(s): equality constraints on leading columns plus an inequality on the next limit the scanned part of the index. Constraints on later columns are still checked inside the index. PostgreSQL (current docs) can also apply a skip scan when the leading column has few distinct values, and SQLite's skip-scan likewise needs many duplicates in the left-most columns; otherwise a query that does not constrain the first column often falls back to a full scan. PostgreSQL advises using multicolumn indexes sparingly and notes indexes with more than three columns rarely help.
- B-tree indexes can return rows already sorted, so an `ORDER BY` matching the index can skip the sort, and `ORDER BY ... LIMIT n` can fetch the first rows directly. For queries reading a large fraction of the table an explicit sort is likely faster than the index. Mixed directions such as `ORDER BY x ASC, y DESC` need an index declared with those directions.
- Index foreign key columns (the foreign key declaration does not create the index). Primary key and unique constraints create their own unique index. Selective columns benefit most; a partial index (`CREATE INDEX ... WHERE predicate`) avoids indexing very common values, shrinking the index and speeding updates, and PostgreSQL says a value covering more than a few percent of rows will not use the index anyway.
- Each index must be maintained on writes and takes space; look for unused ones with `pg_stat_user_indexes` (`idx_scan`, the number of scans on that index; `last_idx_scan` gives the time of the last one) after observing a full business cycle.
- Verify with `EXPLAIN`; a sequential scan is the right plan when a query has no `WHERE` clause or needs most of the table.
- Deeper design: see indexing-strategy-and-composite-indexes.

## Checked

2026-11-08. Read: PostgreSQL 11.2 Index Types (B-tree section), 11.3 Multicolumn Indexes, 11.4 Indexes and ORDER BY, 11.7 Expression indexes, 11.8 Partial Indexes (intro), the `idx_scan` entries of the cumulative statistics views, and the first part of Using EXPLAIN; SQLite query optimizer overview (WHERE clause analysis, skip-scan section). SQLite claims rest on the optimizer overview only (the SQLite expression-index and partial-index pages were not read). Removed unconfirmed claims: implicit casts defeating indexes, the Oracle/MySQL skip-scan mention, the PostgreSQL version for skip scan, and "low-cardinality booleans rarely benefit".
Method: documentation only; no commands were run.
