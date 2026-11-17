---
id: computing-software.database-administration.sql.recursive-cycle-detection
name: recursive-cycle-detection
category: computing-software
field: database-administration
product: sql
tags: [sql, recursive-cycle-detection]
level: advanced
status: docs-checked
description: "Prevent infinite recursion on cyclic graphs using CYCLE or path checks."
sources: ["https://www.postgresql.org/docs/current/queries-with.html", "https://learn.microsoft.com/en-us/sql/t-sql/queries/with-common-table-expression-transact-sql"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cycle detection and termination in recursive CTEs

- PostgreSQL: `WITH RECURSIVE ... ) CYCLE id SET is_cycle USING path SELECT ...` names the columns to track, a flag column showing a cycle was detected, and a path column; both are added to the CTE output and the query is rewritten to the array form below. The manual does not give the release that introduced CYCLE, so check the release notes for your version.
- Portable form the manual calls standard: carry an array of visited values (`path || g.id`), set `g.id = ANY(path)` as an `is_cycle` flag and add `AND NOT is_cycle` to the recursive term. For multi-column keys use an array of `ROW(...)`; for one key column omit ROW, which is more efficient.
- `UNION` (not `UNION ALL`) discards rows duplicating a previous result row, but a cycle often involves no fully duplicate row, and an output depth column means switching to UNION would not stop the loop.
- Testing trick: put a LIMIT in the parent query. PostgreSQL evaluates only as many WITH rows as are fetched, but the manual says not to rely on this in production, and it fails if the outer query sorts or joins the recursive result.
- SQL Server: bound recursion with `OPTION (MAXRECURSION n)`, n from 0 to 32767; the server default is 100 and 0 means no limit.
- Self-check: insert a cycle on purpose and confirm the query terminates.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual page queries-with.html (cycle handling section) and the Microsoft Learn page WITH common_table_expression (recursive guidelines); the draft's PostgreSQL 14 version claim and depth-limit tip are not on those pages and were removed.
