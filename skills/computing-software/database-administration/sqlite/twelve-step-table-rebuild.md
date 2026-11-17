---
id: computing-software.database-administration.sqlite.twelve-step-table-rebuild
name: twelve-step-table-rebuild
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-alter-table, table-rebuild-procedure, schema-change, foreign-keys, legacy-alter-table, drop-column, alter-column-type]
level: advanced
status: verified
description: "Make SQLite schema changes ALTER TABLE cannot do (change type, add constraint, alter PK) with the official 12-step rebuild, keeping foreign keys, indexes and triggers intact."
sources:
  - https://sqlite.org/lang_altertable.html#otheralter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The 12-step table rebuild

**Goal:** change a column type, add a CHECK/FK, or reorder a primary key in SQLite
without breaking references.

## What ALTER TABLE can do natively
`RENAME TABLE`, `RENAME COLUMN` (3.25+), `ADD COLUMN` (with limits: no PK/UNIQUE,
no default of CURRENT_TIMESTAMP or a parenthesised expression, `NOT NULL` needs a non-NULL default, no STORED generated column), `DROP COLUMN` (3.35+, not for PK/UNIQUE/indexed/FK
columns, columns named in a table-level CHECK, partial-index WHERE, generated column, trigger or view). Everything else needs a rebuild.
Tested on 3.50.4: on a table with rows `ADD COLUMN ... DEFAULT (datetime('now'))` and `DEFAULT current_timestamp` failed with `Cannot add a column with non-constant default` (on an empty table they were accepted), `ADD COLUMN x TEXT PRIMARY KEY` / `UNIQUE` failed (`Cannot add a PRIMARY KEY column`), a NOT NULL column without default failed, `STORED` failed (`cannot add a STORED column`), while `ADD COLUMN ... CHECK` and a VIRTUAL generated column worked. Dropping an indexed column failed (`error in index ai after drop column`), a table-level `FOREIGN KEY(pid)` column failed, a table-level CHECK column failed, the PK failed (`cannot drop PRIMARY KEY column`).

## Procedure (from the SQLite docs, condensed)
```sql
PRAGMA foreign_keys = OFF;                -- 1. must be outside a transaction
BEGIN;                                    -- 2.
-- 3. remember indexes/triggers/views:
SELECT type, name, sql FROM sqlite_schema WHERE tbl_name = 'orders';
CREATE TABLE new_orders (                 -- 4. desired definition
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  amount_cents INTEGER NOT NULL CHECK (amount_cents >= 0),
  created_at TEXT NOT NULL
);
INSERT INTO new_orders (id, customer_id, amount_cents, created_at)       -- 5. copy
  SELECT id, customer_id, CAST(round(amount*100) AS INTEGER), created_at FROM orders;
-- 5b. DROP VIEW (and triggers on OTHER tables) that mention orders, or SET legacy_alter_table=ON
DROP TABLE orders;                        -- 6.
ALTER TABLE new_orders RENAME TO orders;  -- 7.
-- 8. recreate indexes and triggers of this table from step 3
CREATE INDEX orders_customer ON orders(customer_id);
-- 9. recreate the views dropped before step 6 (see warning below)
PRAGMA foreign_key_check;                 -- 10. must return no rows
COMMIT;                                   -- 11.
PRAGMA foreign_keys = ON;                 -- 12.
```

## Views and triggers that mention the table (tested, this is where the condensed list above fails)
Run exactly as listed, with a view `v AS SELECT * FROM orders` or a trigger on another table that selects from `orders`, step 7 fails on 3.50.4 with `error in view v: no such table: main.orders` (or `error in trigger trg: ...`) and the transaction must roll back. sqlite.org says to `DROP VIEW` any view affected by the change before dropping the old table and recreate it after. Do the same for triggers on other tables that refer to `orders`. The alternative that worked in the test is `PRAGMA legacy_alter_table=ON` before the rename (the rebuild then committed with `foreign_key_check` empty and `integrity_check` ok), then back to OFF.

## Why this order
- Creating the new table under a temporary name and renaming it **into** place
  (not renaming the old one away) keeps other tables' foreign keys pointing at
  `orders` by name. Renaming the old table first would rewrite references in other
  tables to the old name (since 3.26, unless `legacy_alter_table=ON`). Tested: with `foreign_keys=OFF` and `legacy_alter_table=OFF` a `REFERENCES cust(id)` in another table became `REFERENCES "cust_old"(id)`; with `foreign_keys=OFF` and `legacy_alter_table=ON` it was left alone; with `foreign_keys=ON` it was rewritten in both cases.
- Foreign keys off, so DROP TABLE does not cascade or fail; foreign_key_check
  verifies integrity before commit.

## Gotchas
- `PRAGMA foreign_keys` is a no-op inside a transaction: set it before BEGIN (checked: after `BEGIN; PRAGMA foreign_keys=OFF` it still returned 1).
- Migration frameworks (Alembic batch mode, Django) implement this; make sure
  they also copy triggers.
- Large tables: needs free disk ~ table size; runs under a write lock.

## Verify
`PRAGMA integrity_check;` returns ok, `PRAGMA foreign_key_check;` empty,
`sqlite_schema` shows the new definition and the recreated indexes.
