---
id: computing-software.database-administration.sql.index-column-order
name: index-column-order
category: computing-software
field: database-administration
product: sql
tags: [sql, index-column-order]
level: practitioner
status: docs-checked
description: "Order composite index columns by equality, then range, then sort."
sources: ["https://www.postgresql.org/docs/current/indexes-multicolumn.html", "https://www.sqlite.org/queryplanner.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing multicolumn index column order

- PostgreSQL B-tree: a multicolumn index can be used for any subset of its columns, but is most efficient with constraints on the leading (leftmost) columns. Equality constraints on leading columns, plus inequality constraints on the first column without an equality constraint, always limit the portion of the index scanned; constraints on columns further right are checked inside the index but need not reduce the scanned range. So order columns equality first, then the range column.
- PostgreSQL may apply a skip scan so that a condition only on a later column (an index on `(x, y)` with `WHERE y = 7700`) can still use the index, generally only when the leading column has few distinct values; otherwise expect a full index scan or a sequential scan.
- SQLite: the leftmost column orders the index, later columns break ties. A query on the left-most column alone can use the index, which is why SQLite's planner page says never keep two indexes where one is a prefix of the other (drop the shorter). Where a filter and an `ORDER BY` can both be served, `WHERE fruit='Orange' ORDER BY state` on index `(fruit, state)` needs no separate sort.
- PostgreSQL warns to use multicolumn indexes sparingly: a single-column index is usually sufficient, and more than three columns is unlikely to help unless the workload is very stylised.
- Self-check: EXPLAIN shows the index condition covering the leading columns you intended.

## Checked

Date: 2026-11-07. Read PostgreSQL 11.3 Multicolumn Indexes in full and the SQLite Query Planner sections on multi-column indexes, prefix rule and search-plus-sort (1.6 and 3.1). Removed: "selectivity alone is not the rule" and "prefer one composite over several single-column indexes" (the PostgreSQL page advises the opposite: sparingly). The "range column stops later columns seeking" line is restated from the PostgreSQL equality/inequality rule. Put-ORDER-BY-columns-last is only shown by the SQLite example, not stated as a general rule.
Method: documentation only; no commands were run.
