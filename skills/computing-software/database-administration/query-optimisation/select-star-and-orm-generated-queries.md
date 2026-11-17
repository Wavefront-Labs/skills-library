---
id: computing-software.database-administration.query-optimisation.select-star-and-orm-generated-queries
name: select-star-and-orm-generated-queries
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, select-star, orm-queries, column-projection, covering-index, query-patterns]
level: practitioner
status: draft
description: "Find and fix SELECT * and ORM-generated query problems: wide rows, lost index-only scans, lazy-loading storms, giant IN lists and unbounded queries."
sources:
  - https://use-the-index-luke.com/sql/clustering/index-only-scan-covering-index
  - https://docs.djangoproject.com/en/stable/topics/db/optimization/
  - https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SELECT * and ORM-generated query problems

## Why SELECT * costs
- Transfers and deserialises every column, including large text/JSON/BLOB columns (TOAST fetches in PostgreSQL, LOB reads elsewhere).
- Prevents index-only/covering scans: the database must visit the table for columns you do not use.
- Breaks when columns are added (positional consumers) and leaks new sensitive columns into APIs.
- Larger rows mean bigger sorts and hashes (spills sooner).

Select the columns you need; in views, list columns explicitly.

## ORM patterns to watch
| Pattern | Symptom | Fix |
|---|---|---|
| Lazy loading in loops (N+1) | Hundreds of identical small queries per request | Eager loading: Django `select_related`/`prefetch_related`, SQLAlchemy `selectinload`/`joinedload`, Rails `includes`, EF `Include` |
| Loading entities to read one field | `SELECT *` of wide rows | Django `.only()`/`.values()`, SQLAlchemy `load_only()`, EF projections `Select(x => new {...})` |
| Counting by loading | `len(qs)` / `.ToList().Count` | `.count()` / `COUNT(*)` |
| Existence by loading | `if qs:` | `.exists()` → `SELECT 1 ... LIMIT 1` |
| Giant IN lists from prefetch | `WHERE id IN (...50,000 ids...)` | Batch size limits, joins, temp tables or `= ANY(array)` |
| Unbounded queries | Fetches entire table for "recent items" | Always `ORDER BY ... LIMIT`; keyset pagination |
| Implicit type casts | ORM binds `varchar` param against `nvarchar` (SQL Server) or text vs uuid | Map types correctly; check plans for `CONVERT_IMPLICIT` |
| Updating all columns | `UPDATE ... SET every column` | Dirty tracking / partial updates (`update_fields`) |

## Finding them
- Log SQL in development (Django Debug Toolbar, SQLAlchemy `echo=True`, Rails logs, EF `LogTo`) and count queries per request in tests (`assertNumQueries`).
- In production: `pg_stat_statements` / Performance Schema digests / Query Store, sorted by calls and total time; look for statements with huge call counts and identical shapes.
- APM traces showing many DB spans per request.

## Verify
Per-request query count and bytes transferred drop; plans for the fixed queries show index-only scans where a covering index exists.
