---
id: computing-software.database-administration.query-optimisation.descending-index-order-and-nulls-first
name: descending-index-order-and-nulls-first
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, descending-index-order, mixed-sort-index, nulls-first, indexing, order-by]
level: practitioner
status: draft
description: "Design multi-column indexes with ASC/DESC and NULLS FIRST/LAST that match mixed-direction ORDER BY clauses, so the database reads the index in order and skips the sort."
sources:
  - https://use-the-index-luke.com/sql/sorting-grouping/order-by-asc-desc-nulls-last
  - https://www.postgresql.org/docs/current/indexes-ordering.html
  - https://dev.mysql.com/doc/refman/8.4/en/descending-indexes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ASC / DESC and NULLS FIRST in multi-column indexes

## Single direction is free
An index on `(created_at)` serves both `ORDER BY created_at` and `ORDER BY created_at DESC` (scanned backwards). Same for `(a, b)` with `ORDER BY a DESC, b DESC`.

## Mixed directions need a matching index
```sql
SELECT * FROM posts WHERE forum_id = 7 ORDER BY pinned DESC, created_at ASC LIMIT 20;
CREATE INDEX posts_forum_pinned_created ON posts (forum_id, pinned DESC, created_at ASC);
```
An index `(forum_id, pinned, created_at)` cannot deliver `pinned DESC, created_at ASC` order (neither forward nor backward scan matches), so the database sorts all matching rows before `LIMIT`.

Engine support:
- PostgreSQL, SQL Server, Oracle, SQLite: honour per-column DESC.
- MySQL: DESC in index definitions is honoured only from **8.0**; 5.7 parsed and ignored it.

## NULL ordering
- PostgreSQL default: ASC = NULLS LAST, DESC = NULLS FIRST. `ORDER BY score DESC NULLS LAST` needs `CREATE INDEX ON t (score DESC NULLS LAST)`; otherwise a sort appears.
- Oracle same defaults as PostgreSQL; SQL Server/MySQL/SQLite treat NULL as smallest (first in ASC) without NULLS syntax support in indexes (MySQL/SQL Server lack NULLS FIRST/LAST in ORDER BY; SQLite supports it in ORDER BY since 3.30).
- If NULLs are impossible, add `NOT NULL` so the question disappears.

## Keyset pagination
Mixed-direction keyset conditions get awkward (`(a, b) > (x, y)` row comparison assumes same direction). Prefer same-direction sort keys (e.g. negate a numeric column into a generated column) for clean seek predicates.

## Verify
`EXPLAIN` shows `Index Scan` (or `Index Scan Backward`) with no `Sort` node above it and execution stopping after the LIMIT rows (`actual rows=20`).
