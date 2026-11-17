---
id: computing-software.database-administration.sql.insert-select-and-multirow
name: insert-select-and-multirow
category: computing-software
field: database-administration
product: sql
tags: [sql, insert-select-and-multirow]
level: intro
status: docs-checked
description: "Insert many rows with multi-row VALUES and INSERT ... SELECT."
sources: ["https://www.postgresql.org/docs/current/sql-insert.html", "https://www.sqlite.org/lang_insert.html", "https://www.sqlite.org/limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# INSERT SELECT and multi-row VALUES

- `INSERT INTO t (a,b) VALUES (1,'x'), (2,'y');` inserts several rows in one statement (PostgreSQL documents the multirow VALUES syntax; SQLite's VALUES form "creates one or more new rows"). `INSERT INTO t (a,b) SELECT ... FROM s WHERE ...;` inserts one row per row the query returns.
- List the columns. Without a list the values map onto the table's columns in declared order (PostgreSQL), or must equal the column count (SQLite), so adding or reordering a column can break the statement. Columns not listed get their default or NULL.
- `INSERT INTO t DEFAULT VALUES;` inserts one row of defaults (NULL where no default exists in SQLite). In SQLite it is not allowed with an upsert clause.
- SQLite: with an upsert clause the `SELECT` form needs a `WHERE` clause (even `WHERE true`) to avoid parsing `ON` as a join constraint.
- SQLite limits host parameter numbers via `SQLITE_MAX_VARIABLE_NUMBER`: 999 before 3.32.0, 32766 from 3.32.0, which caps the placeholders in a big multi-row insert.
- Self-check: compare `count(*)` before and after with the rows inserted.

## Checked

Date: 2026-11-07. Read the PostgreSQL INSERT description, synopsis, DEFAULT VALUES and query parameters and the multirow example list (by search), SQLite lang_insert (the three forms and the upsert note) and the SQLite limits entry for host parameters. Confirmed the items above. Corrected: the variable limit is "after 3.32.0 (2020-05-22) 32766, 999 before" per the page; added the SQLite upsert/WHERE and DEFAULT VALUES details. The "list columns" advice is practice grounded in the pages' column-mapping rules.
Method: documentation only; no commands were run.
