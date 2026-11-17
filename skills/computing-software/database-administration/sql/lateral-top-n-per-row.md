---
id: computing-software.database-administration.sql.lateral-top-n-per-row
name: lateral-top-n-per-row
category: computing-software
field: database-administration
product: sql
tags: [sql, lateral-top-n-per-row]
level: advanced
status: docs-checked
description: "Use LATERAL subqueries with LIMIT to fetch the latest N child rows per parent."
sources: ["https://www.postgresql.org/docs/current/queries-table-expressions.html", "https://www.postgresql.org/docs/current/indexes-ordering.html", "https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LATERAL for top-N per parent row

- `SELECT c.id, o.* FROM customers c CROSS JOIN LATERAL (SELECT * FROM orders o WHERE o.cid = c.id ORDER BY o.ts DESC LIMIT 3) o;` Without `LATERAL`, a subquery in `FROM` cannot reference earlier `FROM` items; with it, the subquery is evaluated per outer row.
- `LEFT JOIN LATERAL (...) ON true` keeps parents whose subquery returns no rows (PostgreSQL's documented pattern); a cross join drops them.
- An index on `orders(cid, ts)` lets each probe read the first rows in order: a B-tree can be scanned backward to satisfy `ORDER BY ts DESC`, and `ORDER BY ... LIMIT n` can stop after n rows.
- SQL Server spells this `CROSS APPLY` / `OUTER APPLY`: the right side is evaluated against every row of the left. `CROSS` produces no rows for an empty result, `OUTER` still produces one row per left row.
- Self-check: run EXPLAIN and confirm the subquery is an index scan with a Limit inside a Nested Loop, not a sort of the whole table.

## Checked

2026-11-08. Confirmed on the PostgreSQL table expressions page: `LATERAL` semantics and `LEFT JOIN LATERAL ... ON true`. Confirmed on the PostgreSQL index ordering page: backward scans and `ORDER BY ... LIMIT`. Confirmed on the Microsoft FROM clause page: `CROSS APPLY` and `OUTER APPLY`. Removed the claim that SQLite lacks LATERAL (the SQLite SELECT page was not fully readable) and the `ts DESC` index declaration, which a plain backward scan makes unnecessary here.
Method: documentation only; no commands were run.
