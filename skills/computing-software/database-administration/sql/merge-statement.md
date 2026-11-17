---
id: computing-software.database-administration.sql.merge-statement
name: merge-statement
category: computing-software
field: database-administration
product: sql
tags: [sql, merge-statement]
level: advanced
status: docs-checked
description: "Use SQL standard MERGE for conditional insert, update and delete."
sources: ["https://www.postgresql.org/docs/current/sql-merge.html", "https://www.postgresql.org/docs/15/release-15.html", "https://www.postgresql.org/docs/17/release-17.html", "https://learn.microsoft.com/en-us/sql/t-sql/statements/merge-transact-sql", "https://www.sqlite.org/lang.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MERGE statement

- `MERGE INTO t USING s ON t.id = s.id WHEN MATCHED THEN UPDATE SET v = s.v WHEN NOT MATCHED THEN INSERT (id, v) VALUES (s.id, s.v);` PostgreSQL added `MERGE` in 15; SQL Server has it too.
- `WHEN MATCHED AND cond THEN DELETE` is allowed.
- PostgreSQL 17 added a `RETURNING` clause (with `merge_action()`) and `WHEN NOT MATCHED BY SOURCE`; `RETURNING`, `BY SOURCE`/`BY TARGET` and `DO NOTHING` are extensions to the SQL standard.
- SQLite's list of SQL statements has no `MERGE`.
- Cardinality: a target row should join to at most one source row. Otherwise a repeated `UPDATE` or `DELETE` raises a cardinality error and a repeated `INSERT` a uniqueness violation.
- Concurrency: PostgreSQL applies the usual transaction isolation rules and suggests `INSERT ... ON CONFLICT` when you need an update on a concurrent insert; the two are not interchangeable. SQL Server notes that `HOLDLOCK` (SERIALIZABLE) can prevent unique key violations when keys are both inserted and updated, and that under heavy concurrency separate `INSERT`/`UPDATE`/`DELETE` statements may block less.
- Self-check: source rows must be unique on the join key.

## Checked

2026-11-08. Confirmed on the PostgreSQL MERGE page: syntax, `WHEN MATCHED AND ... THEN DELETE`, cardinality and uniqueness errors, concurrency note, standard extensions. PostgreSQL 15 and 17 release notes confirm the version claims. Microsoft MERGE page confirms the `HOLDLOCK` guidance. Removed "Oracle" and "MySQL" (not read), and the unqualified claim that MERGE is not atomic in all engines. The SQLite statement list (lang.html) shows no `MERGE`.
Method: documentation only; no commands were run.
