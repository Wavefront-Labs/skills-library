---
id: computing-software.database-administration.sql.sql-constraints-keys-and-integrity
name: sql-constraints-keys-and-integrity
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-constraints, primary-key, foreign-key, check-constraint, unique-constraint]
level: practitioner
status: docs-checked
description: "Enforce integrity in the schema with PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL and CHECK constraints."
sources: ["https://www.postgresql.org/docs/current/ddl-constraints.html", "https://www.postgresql.org/docs/current/sql-createtable.html", "https://www.postgresql.org/docs/current/sql-altertable.html", "https://www.sqlite.org/foreignkeys.html", "https://www.sqlite.org/nulls.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constraints

- `PRIMARY KEY` = unique + not null (PostgreSQL creates a unique B-tree index and marks the columns NOT NULL). A table has at most one; any number of `UNIQUE` constraints are allowed. PostgreSQL does not enforce having a primary key but advises it. A primary key is the default target of a foreign key that names no column list. Prefer a narrow surrogate key plus a unique natural key where one exists.
- `UNIQUE`: in PostgreSQL two NULLs are not equal by default, so rows with a NULL in a constrained column can repeat. `UNIQUE NULLS NOT DISTINCT (col)` changes that. The SQL standard leaves the default implementation-defined, and SQLite's NULL-handling survey (dated 2003) found SQLite, PostgreSQL and Oracle treat NULLs as distinct in UNIQUE columns while MS-SQL and Informix did not, so re-test portable schemas on each engine. A uniqueness rule for only some rows cannot be a unique constraint; use a unique partial index.
- `FOREIGN KEY (c) REFERENCES p (id) ON DELETE CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION`. The default is `NO ACTION`. `RESTRICT` cannot be deferred; `NO ACTION` can. `ON DELETE SET NULL (col)` can name which columns to null (PostgreSQL), useful when part of the key is in the primary key. By default a referencing row with any NULL key column escapes the check; `MATCH FULL` or `NOT NULL` closes that gap.
- The referenced columns must be a primary key or a unique constraint/non-partial unique index. The referencing columns are not indexed automatically in PostgreSQL or SQLite, and parent deletes or key updates scan the child table, so create that index yourself.
- SQLite does not enforce foreign keys unless `PRAGMA foreign_keys = ON` is run; it is off by default and must be set for each database connection.
- `CHECK (qty > 0)` passes when the expression is true or NULL, so pair it with `NOT NULL`. PostgreSQL does not support a CHECK that looks at other rows or tables (use UNIQUE, EXCLUDE or FOREIGN KEY, or a trigger for a one-off check), and assumes CHECK expressions are immutable: changing a function used in a CHECK is not detected, so drop and re-add the constraint.
- Make most columns `NOT NULL`: the PostgreSQL docs say the majority of columns in most designs should be.
- `DEFERRABLE INITIALLY DEFERRED` postpones the check to the end of the transaction (useful for circular inserts). PostgreSQL accepts it only on UNIQUE, PRIMARY KEY, EXCLUDE and FOREIGN KEY constraints, not NOT NULL or CHECK; SQLite supports it on foreign keys.
- Adding a constraint to a large live PostgreSQL table: `ALTER TABLE ... ADD CONSTRAINT ... NOT VALID` skips the lengthy scan of existing rows (new writes are still checked; allowed for foreign-key, CHECK and not-null constraints), then `VALIDATE CONSTRAINT` later. `ADD FOREIGN KEY` takes a `SHARE ROW EXCLUSIVE` lock, most other forms `ACCESS EXCLUSIVE`.

## Checked

2026-11-08. Read in full: PostgreSQL 5.5 Constraints. Read the relevant sections only of the PostgreSQL `ALTER TABLE` (`ADD table_constraint`, `VALIDATE CONSTRAINT`) and `CREATE TABLE` (`DEFERRABLE`, `ON DELETE`) pages, the SQLite foreign key page (overview, enabling, indexing, deferral and action sections) and the SQLite NULL handling comparison table. Removed unconfirmed claims: PostgreSQL 15 version tag, MySQL UNIQUE behaviour, "Oracle supports DEFERRABLE", and "constraints are documentation the optimiser can use".
Method: documentation only; no commands were run.
