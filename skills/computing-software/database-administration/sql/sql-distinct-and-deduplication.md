---
id: computing-software.database-administration.sql.sql-distinct-and-deduplication
name: sql-distinct-and-deduplication
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-deduplication, distinct-on, row-number-dedupe, delete-duplicates]
level: practitioner
status: docs-checked
description: "Find and remove duplicate rows with GROUP BY, ROW_NUMBER and DISTINCT ON, then prevent them with constraints."
sources: ["https://www.postgresql.org/docs/current/sql-select.html", "https://www.postgresql.org/docs/current/sql-delete.html", "https://www.postgresql.org/docs/current/ddl-system-columns.html", "https://www.postgresql.org/docs/current/functions-window.html", "https://www.sqlite.org/lang_select.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Duplicates

- Find: `SELECT key, COUNT(*) FROM t GROUP BY key HAVING COUNT(*) > 1;`
- Keep one, portable form: number rows per key with a window function and delete those after the first, identified by the primary key:
  `WITH r AS (SELECT id, ROW_NUMBER() OVER (PARTITION BY key ORDER BY created_at DESC) rn FROM t) DELETE FROM t WHERE id IN (SELECT id FROM r WHERE rn > 1);`
  `row_number()` numbers the rows of each partition from 1. PostgreSQL also lets `DELETE ... USING` reference other tables or a CTE in the WHERE condition.
- With no usable key in PostgreSQL, `ctid` (the physical row location) can be matched inside one statement, but the docs warn it changes when a row is updated or moved by `VACUUM FULL` and should not be used as a row identifier; add a primary key afterwards.
- Select-only dedupe in PostgreSQL: `SELECT DISTINCT ON (key) * FROM t ORDER BY key, created_at DESC;` It keeps the first row of each group of equal `key`, and the first row is unpredictable without `ORDER BY`. The `DISTINCT ON` expressions must match the leftmost `ORDER BY` expressions. It is a PostgreSQL extension to standard SQL; elsewhere filter `ROW_NUMBER() = 1` in a subquery or CTE.
- `SELECT DISTINCT` removes duplicate rows. In SQLite duplicates are detected as with `IS DISTINCT FROM`, so two NULLs count as equal.
- `UNION` removes duplicate rows from the result; `UNION ALL` keeps them and PostgreSQL notes it is usually significantly quicker, so use ALL when you can.
- After cleaning, add a `UNIQUE` constraint or unique index so duplicates cannot recur. By default PostgreSQL treats NULLs as distinct in unique constraints (`NULLS NOT DISTINCT` changes this), so NULL keys can still repeat.
- Preview with a `SELECT` of the rows to delete, and take a backup or run in a transaction.

## Checked

2026-11-08. Read: PostgreSQL `SELECT` (`DISTINCT` clause, `UNION` clause), `DELETE` (`USING`), 5.6 System Columns (`ctid`), 9.22 window functions (`row_number`); SQLite `SELECT` (duplicate removal section, compound select intro); SQLite window functions page (`row_number()` example). Removed unconfirmed claims: `rowid` as a SQLite/Oracle row identifier, expression-index/generated-column normalisation, and that UNION costs a sort or hash. The original `ctid` delete was replaced with a primary-key form because of the `ctid` warning.
Method: documentation only; no commands were run.
