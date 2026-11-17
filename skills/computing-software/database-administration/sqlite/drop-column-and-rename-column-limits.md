---
id: computing-software.database-administration.sqlite.drop-column-and-rename-column-limits
name: drop-column-and-rename-column-limits
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, drop-column-sqlite, rename-column, alter-table, sqlite-schema, schema-migrations]
level: practitioner
status: verified
description: "Use SQLite ALTER TABLE DROP COLUMN (3.35+) and RENAME COLUMN (3.25+), know which columns cannot be dropped, and fall back to the 12-step rebuild."
sources:
  - https://sqlite.org/lang_altertable.html
  - https://sqlite.org/lang_altertable.html#otheralter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ALTER TABLE DROP COLUMN and RENAME COLUMN

## What ALTER TABLE supports
```sql
ALTER TABLE users RENAME TO accounts;                 -- any version
ALTER TABLE users RENAME COLUMN fullname TO name;     -- 3.25.0+
ALTER TABLE users ADD COLUMN last_login TEXT;         -- with restrictions
ALTER TABLE users DROP COLUMN legacy_flag;            -- 3.35.0+
```
Check the runtime version, not the CLI's: `SELECT sqlite_version();` inside the app (Python, Android and iOS bundle older libraries).

## RENAME COLUMN
Rewrites references in indexes, triggers, views and foreign keys. With `PRAGMA legacy_alter_table=ON`, `RENAME TABLE` stops rewriting views and trigger bodies (RENAME COLUMN still does); keep it OFF.

## DROP COLUMN fails when the column
- is a PRIMARY KEY or part of one, or has a UNIQUE constraint;
- is indexed (drop the index first);
- appears in a partial index WHERE, a CHECK constraint (other than the column's own), a generated column expression, a trigger or view;
- is used in a table-level FOREIGN KEY constraint (a column-level `REFERENCES` clause goes away with the column).
DROP COLUMN rewrites the whole table to remove the data (cost proportional to table size, needs free disk space) and runs inside a transaction.

## ADD COLUMN restrictions
ADD COLUMN can never add PRIMARY KEY or UNIQUE columns. On a table that already has rows it also rejects non-constant defaults (`CURRENT_TIMESTAMP`, `CURRENT_DATE`, parenthesised expressions), `NOT NULL` without a non-NULL default, and STORED generated columns (an empty table accepted all three). It is O(1): it edits the schema text only.

## Fallback: 12-step rebuild
For type changes, constraint changes or blocked drops: `PRAGMA foreign_keys=OFF`, `BEGIN`, create new table, `INSERT INTO new SELECT ...`, drop old, rename new, recreate indexes/triggers/views, `PRAGMA foreign_key_check`, `COMMIT`, `PRAGMA foreign_keys=ON`.

## Verify
After the migration: `PRAGMA integrity_check;`, `PRAGMA foreign_key_check;`, and `.schema users` shows the expected column list.

## Checked
- SQLite 3.50.4: `RENAME COLUMN` rewrote a view and a trigger; `DROP COLUMN` failed for a PRIMARY KEY, a UNIQUE column, an indexed column, a column used in a view, a generated expression, a partial-index WHERE, another column's CHECK and a table-level FOREIGN KEY, and succeeded for a column with its own CHECK, an inline `REFERENCES` and a generated column itself; ADD COLUMN rejects PRIMARY KEY, UNIQUE, non-constant defaults (including `(1+1)` and `CURRENT_DATE`), NOT NULL without default and STORED generated columns, allows VIRTUAL generated ones, and these checks only fire when the table has rows; `legacy_alter_table=ON` stops `RENAME TABLE` rewriting views and trigger bodies but not `RENAME COLUMN`. Release logs: 3.25.0 RENAME COLUMN, 3.35.0 DROP COLUMN.
