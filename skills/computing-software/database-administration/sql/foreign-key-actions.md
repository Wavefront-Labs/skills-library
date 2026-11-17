---
id: computing-software.database-administration.sql.foreign-key-actions
name: foreign-key-actions
category: computing-software
field: database-administration
product: sql
tags: [sql, foreign-key-actions]
level: practitioner
status: docs-checked
description: "Choose CASCADE, SET NULL, RESTRICT and NO ACTION for foreign keys."
sources: ["https://www.postgresql.org/docs/current/ddl-constraints.html", "https://www.postgresql.org/docs/current/sql-createtable.html", "https://www.sqlite.org/foreignkeys.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Foreign key ON DELETE and ON UPDATE actions

- `FOREIGN KEY (cid) REFERENCES customers (id) ON DELETE CASCADE`; options: `NO ACTION` (the default in both PostgreSQL and SQLite), `RESTRICT`, `SET NULL`, `SET DEFAULT`.
- PostgreSQL: with `NO ACTION` the deletion may proceed but the constraint must still hold when it is checked (immediately, or later if deferred). `RESTRICT` prevents the action and cannot be deferred; it also blocks an update to a value that is distinct but compares equal. `SET DEFAULT` fails if the default value has no matching referenced row. `SET NULL` / `SET DEFAULT` can take a column list, for `ON DELETE` only.
- SQLite: `RESTRICT` errors immediately, even when the constraint is deferred; `NO ACTION` takes no special action and leaves the normal immediate or deferred constraint check.
- Index the referencing (child) columns: a `DELETE` of a parent row or `UPDATE` of a referenced column needs a scan of the child table to find matching rows, and PostgreSQL does not create that index for you; SQLite says the child key index need not be `UNIQUE`.
- `DEFERRABLE INITIALLY DEFERRED` checks at the end of the transaction (PostgreSQL and SQLite). In SQLite outside an explicit transaction a deferred constraint behaves like an immediate one.
- SQLite enforces foreign keys only after `PRAGMA foreign_keys = ON`; it is off by default and must be enabled separately for each database connection.
- Self-check: delete a parent in a test and confirm the intended child outcome.

## Checked

Date: 2026-11-07. Read the Foreign Keys section of the PostgreSQL Constraints page (ddl-constraints, from the ON DELETE example to the index paragraph), the foreign-key action and DEFERRABLE parameter text of CREATE TABLE (sql-createtable, by search with the action paragraphs read), and SQLite foreignkeys sections 2 (Enabling), 4.2 (Deferred), the child-key index paragraph and the ON DELETE/ON UPDATE actions section (rest of the page searched, not read in full). Confirmed all items above. Corrected: "NO ACTION ... checked at statement end" and "RESTRICT (immediate)" were replaced by the pages' wording (NO ACTION is checked at constraint check time and can be deferred; RESTRICT is not deferrable); "deletes of parents scan the child table" now states what the pages say.
Method: documentation only; no commands were run.
