---
id: computing-software.database-administration.sql.limit-offset-fetch
name: limit-offset-fetch
category: computing-software
field: database-administration
product: sql
tags: [sql, limit-offset-fetch]
level: intro
status: docs-checked
description: "Limit result rows with LIMIT/OFFSET or the standard FETCH FIRST clause."
sources: ["https://www.postgresql.org/docs/current/queries-limit.html", "https://www.postgresql.org/docs/current/sql-select.html", "https://www.postgresql.org/docs/13/release-13.html", "https://learn.microsoft.com/en-us/sql/t-sql/queries/select-order-by-clause-transact-sql"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LIMIT OFFSET and FETCH FIRST

- `LIMIT n OFFSET m` is PostgreSQL-specific syntax also used by MySQL. The SQL:2008 standard form is `OFFSET m ROWS FETCH FIRST n ROWS ONLY`, which PostgreSQL also accepts (in either clause order; the standard puts `OFFSET` first) and DB2 uses.
- SQL Server has no `LIMIT`: `OFFSET m ROWS FETCH NEXT n ROWS ONLY` is part of `ORDER BY`, so it requires one (SQL Server 2012 and later). Its `FETCH` takes only `ONLY`, and it cannot be combined with `TOP` in the same scope.
- `FETCH FIRST n ROWS WITH TIES` also returns rows tying with the last one; `ORDER BY` is mandatory. Added in PostgreSQL 13.
- Always pair with a unique `ORDER BY`; otherwise the subset returned is unpredictable and different pages give inconsistent results.
- Gotcha: rows skipped by `OFFSET` are still computed inside the server, so a large `OFFSET` can be slow; see keyset pagination.
- `LIMIT ALL` and `LIMIT NULL` mean no limit; `OFFSET 0` and `OFFSET NULL` mean no offset (PostgreSQL).
- Self-check: `EXPLAIN` shows a Limit node over a Sort or index scan.

## Checked

2026-11-08. Confirmed: PostgreSQL LIMIT/OFFSET page and SELECT page (syntax origin, `WITH TIES`, ordering rules, OFFSET cost); PostgreSQL 13 release notes (`WITH TIES`); Microsoft ORDER BY page (`OFFSET`/`FETCH` need `ORDER BY`, SQL Server 2012, `ONLY` only, no `TOP` combination). Removed the Oracle claim and the SQLite and MySQL `LIMIT` detail that no page read here supported beyond the PostgreSQL compatibility note.
Method: documentation only; no commands were run.
