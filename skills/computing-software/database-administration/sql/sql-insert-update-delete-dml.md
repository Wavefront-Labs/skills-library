---
id: computing-software.database-administration.sql.sql-insert-update-delete-dml
name: sql-insert-update-delete-dml
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-dml, insert-select, update-from, delete-using, multi-row-insert]
level: practitioner
status: docs-checked
description: "Write correct INSERT, UPDATE and DELETE statements including multi-row, INSERT SELECT and join-based updates."
sources: ["https://www.postgresql.org/docs/current/sql-insert.html", "https://www.postgresql.org/docs/current/sql-update.html", "https://www.postgresql.org/docs/current/sql-delete.html", "https://www.postgresql.org/docs/current/sql-truncate.html", "https://www.sqlite.org/lang_insert.html", "https://www.sqlite.org/lang_update.html", "https://www.sqlite.org/lang_delete.html", "https://www.sqlite.org/lang_returning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DML

- `INSERT INTO t (a, b) VALUES (1, 'x'), (2, 'y');` inserts several rows (PostgreSQL multirow `VALUES`). Always list the columns: without a list, PostgreSQL uses all columns in declared order, so a later `ADD COLUMN` silently changes the meaning. Omitted columns get their declared default or NULL. `INSERT ... SELECT` copies a result set; `DEFAULT VALUES` inserts one all-defaults row (SQLite: top-level statements only, and no upsert clause).
- `RETURNING` returns the inserted, updated or deleted rows, which is how you read back generated keys. It is available in PostgreSQL, and in SQLite from 3.35.0 (2021-03-12), where it is an extension modelled on PostgreSQL. SQLite sends RETURNING rows only after all changes are done, in arbitrary order, and does not report rows changed by triggers or foreign key actions.
- `UPDATE t SET a = 1 WHERE ...`: with no `WHERE`, every row is updated; a `WHERE` matching nothing just affects zero rows. Join form `UPDATE t SET ... FROM u WHERE t.id = u.id` works in PostgreSQL and in SQLite 3.33.0 (2020-08-14) and later, which is not standard SQL and differs in SQL Server and MySQL. In PostgreSQL do not repeat the target table in `FROM` unless you intend a self-join (then alias it). A `SET (a, b) = (sub-SELECT)` sub-query must yield at most one row; zero rows assign NULL.
- `DELETE FROM t WHERE ...`; PostgreSQL's `DELETE ... USING other_table WHERE ...` deletes by reference to other tables (or use a sub-select).
- `TRUNCATE` (PostgreSQL) empties tables faster than an unqualified `DELETE` because it does not scan them, and reclaims space immediately. It takes an `ACCESS EXCLUSIVE` lock, does not fire `ON DELETE` triggers (it fires `ON TRUNCATE` triggers), cannot be used on a table referenced by foreign keys unless those tables are truncated too (`CASCADE` does that), is not MVCC-safe for concurrent snapshots, and is transaction-safe (rolls back). `RESTART IDENTITY` resets owned sequences; `CONTINUE IDENTITY` is the default. If concurrent access is needed, use `DELETE`. In SQLite, a `DELETE` with no `WHERE` and no `RETURNING` on a table without triggers uses a fast "truncate optimization" that erases the table without visiting each row.
- Habit: write the `SELECT` with the same `WHERE` first, check the count, then run the DML inside a transaction and inspect the rows affected before `COMMIT`.
- Large changes in batches to limit locks and log growth (see batched-updates-and-deletes).
- Upsert is separate (`INSERT ... ON CONFLICT`, `MERGE`).
- Foreign keys can block deletes or cascade them; know the `ON DELETE` rule.

## Checked

2026-11-08. Read: PostgreSQL `INSERT` (description, parameters, `OVERRIDING`), `UPDATE` (description and `FROM`/sub-select parameters), `DELETE` (description, `USING`), `TRUNCATE` (in full); SQLite `INSERT` (forms and `DEFAULT VALUES`), `UPDATE` (WHERE and UPDATE-FROM sections), `DELETE` (truncate optimization), `RETURNING` (in full). Removed claims the pages do not support: SQL Server `OUTPUT` and `UPDATE ... JOIN` syntax details, that DELETE "logs each row", and implicit-commit behaviour of TRUNCATE in MySQL and Oracle.
Method: documentation only; no commands were run.
