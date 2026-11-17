---
id: computing-software.database-administration.sql.dialect-limit-top-fetch
name: dialect-limit-top-fetch
category: computing-software
field: database-administration
product: sql
tags: [sql, dialect-limit-top-fetch]
level: intro
status: docs-checked
description: "Translate row limiting between PostgreSQL, SQLite and SQL Server."
sources: ["https://www.postgresql.org/docs/current/sql-select.html", "https://www.postgresql.org/docs/current/queries-limit.html", "https://www.sqlite.org/lang_select.html", "https://learn.microsoft.com/en-us/sql/t-sql/queries/top-transact-sql", "https://learn.microsoft.com/en-us/sql/t-sql/queries/select-order-by-clause-transact-sql"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LIMIT TOP and FETCH across dialects

- PostgreSQL: `LIMIT n [OFFSET m]`, or the standard `OFFSET m ROWS FETCH FIRST n ROWS ONLY` (also `WITH TIES`). `LIMIT ALL` or a NULL count means no limit.
- SQLite: `LIMIT n [OFFSET m]` only (no `FETCH` in its SELECT syntax). A negative LIMIT means no upper bound, and `LIMIT m, n` means offset m, limit n (reversed order, so avoid it).
- SQL Server: `SELECT TOP (n) ...` (optional `PERCENT`, `WITH TIES`), or `ORDER BY ... OFFSET m ROWS FETCH NEXT n ROWS ONLY` (SQL Server 2012 and later). `FETCH` needs the `OFFSET` clause; `TOP` cannot be combined with `OFFSET`/`FETCH` in the same query scope.
- Always add `ORDER BY`: without it PostgreSQL returns an unpredictable subset and SQL Server `TOP` returns the first n rows in an undefined order.
- MySQL and Oracle spellings are not covered here: check their own documentation before translating.
- Use a query builder or ORM dialect layer instead of hand-translation.
- Self-check: run the translated query on each target and compare rows.

## Checked

Date: 2026-11-07. Read the PostgreSQL LIMIT and OFFSET page in full; read the LIMIT section of the PostgreSQL SELECT page and the SQLite SELECT LIMIT section (lang_select section 5; confirmed no occurrence of FETCH on the SQLite page by search); read the SQL Server TOP page up to Limitations and the OFFSET/FETCH arguments, restrictions and paging sections of the ORDER BY page (remaining examples not read). Confirmed all syntax above and the TOP versus OFFSET/FETCH restriction. Removed: Oracle 12c FETCH FIRST/ROWNUM, MySQL LIMIT and DB2 statements, and the "portable FETCH FIRST works in Oracle, DB2" list, because none was checked against that engine's own docs; the description now names the three engines covered.
Method: documentation only; no commands were run.
