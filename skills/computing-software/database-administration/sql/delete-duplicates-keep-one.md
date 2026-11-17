---
id: computing-software.database-administration.sql.delete-duplicates-keep-one
name: delete-duplicates-keep-one
category: computing-software
field: database-administration
product: sql
tags: [sql, delete-duplicates-keep-one]
level: practitioner
status: docs-checked
description: "Remove duplicates safely keeping the lowest id per key."
sources: ["https://www.postgresql.org/docs/current/sql-delete.html", "https://www.postgresql.org/docs/current/ddl-system-columns.html", "https://www.postgresql.org/docs/current/functions-subquery.html", "https://www.sqlite.org/lang_delete.html", "https://www.sqlite.org/lang_expr.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deleting duplicates and keeping one row

- `DELETE FROM users u USING users d WHERE u.email = d.email AND u.id > d.id;` (PostgreSQL: `USING` is a PostgreSQL extension to DELETE) keeps the smallest id.
- Portable: `DELETE FROM t WHERE id NOT IN (SELECT min(id) FROM t GROUP BY email);` (SQLite and PostgreSQL). `NOT IN` yields NULL, never true, when the subquery returns a NULL and no equal value, so ids must be NOT NULL or the delete removes nothing.
- Or number the rows with `row_number() OVER (PARTITION BY email ORDER BY id)` in a subquery and delete those with `rn > 1` by physical row identifier: `ctid` in PostgreSQL (it changes when a row is updated or moved by `VACUUM FULL`, so use it only within the one statement) or `rowid` in SQLite (not available on `WITHOUT ROWID` tables).
- Take a backup or `CREATE TABLE ... AS` copy first; run in a transaction.
- Self-check: the key count equals the row count afterwards.

## Checked

Date: 2026-11-07. Read the SQLite DELETE page in full and the PostgreSQL System Columns page in full; read the PostgreSQL Subquery Expressions page in full; searched PostgreSQL DELETE (USING syntax, "USING and RETURNING clauses are PostgreSQL extensions" and the ctid batch example) and the SQLite expression page (IN/NOT IN matrix and the ROWID section, read those two sections). Confirmed: USING syntax, NOT IN NULL semantics in both engines, ctid instability, rowid unavailable on WITHOUT ROWID tables. Corrected: "ids must be NOT NULL" now explains the NOT IN NULL mechanism; ctid and rowid caveats added from the pages. The row_number name was confirmed on the PostgreSQL window function page; no SQLite window page was read, so no SQLite window claim is made.
Method: documentation only; no commands were run.
