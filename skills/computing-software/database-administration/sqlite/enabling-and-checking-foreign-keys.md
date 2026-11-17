---
id: computing-software.database-administration.sqlite.enabling-and-checking-foreign-keys
name: enabling-and-checking-foreign-keys
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-alter-table, pragma-foreign-keys, foreign-key-check, referential-integrity, fk-actions]
level: practitioner
status: verified
description: "Turn on SQLite foreign key enforcement per connection, find existing violations with PRAGMA foreign_key_check, index child columns, and handle FKs during table rebuilds."
sources:
  - https://www.sqlite.org/foreignkeys.html
  - https://www.sqlite.org/pragma.html#pragma_foreign_key_check
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enabling and checking foreign keys

## Enforcement is OFF by default
For backwards compatibility SQLite parses `REFERENCES` clauses but does not enforce them unless
each **connection** runs:
```sql
PRAGMA foreign_keys = ON;
PRAGMA foreign_keys;          -- 1 = enforcing
```
It cannot be set inside a transaction (silently ignored), and it is per connection: set it in
your connection factory / pool init (e.g. SQLAlchemy `connect` event, Django does it by default
for SQLite, `_foreign_keys=on` in Go mattn driver DSN). Compile-time default can be changed with
`SQLITE_DEFAULT_FOREIGN_KEYS=1`.

## Find existing violations
Data inserted while enforcement was off may already be broken:
```sql
PRAGMA foreign_key_check;                -- all tables: table, rowid, parent, fkid
PRAGMA foreign_key_check(order_items);
PRAGMA foreign_key_list(order_items);    -- defined FKs
```
Fix or delete orphans before turning enforcement on for existing databases.

## Define them well
```sql
CREATE TABLE order_items (
  id       INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  sku      TEXT NOT NULL
);
CREATE INDEX order_items_order_id ON order_items(order_id);   -- needed: FK checks on parent delete scan the child otherwise
```
- The parent key must be the PRIMARY KEY or have a UNIQUE index, or you get
  `foreign key mismatch` errors at DML time.
- Actions: `CASCADE`, `SET NULL`, `SET DEFAULT`, `RESTRICT`, `NO ACTION` (default).
- `DEFERRABLE INITIALLY DEFERRED` defers checks to COMMIT (useful for circular references or
  bulk reloads).

## During schema changes
The 12-step table rebuild (create new, copy, drop old, rename) would fire cascades or fail:
```sql
PRAGMA foreign_keys = OFF;
BEGIN;
-- ... rebuild ...
PRAGMA foreign_key_check;       -- must return nothing before commit
COMMIT;
PRAGMA foreign_keys = ON;
```
`PRAGMA legacy_alter_table` and `ALTER TABLE RENAME` behaviours affect how FK references are
rewritten; on modern versions (3.26+) RENAME updates references in child tables.

## Verify
With enforcement on, inserting a child row with a missing parent fails with
`FOREIGN KEY constraint failed`, and `PRAGMA foreign_key_check` returns no rows.

## Checked
- SQLite 3.50.4: `PRAGMA foreign_keys` defaults to 0; setting it inside a transaction is ignored (value stays 0); `foreign_key_check` returns `(table, rowid, parent, fkid)` for an orphan inserted while off; `foreign_key_list` columns; an orphan insert fails with `FOREIGN KEY constraint failed` once on; CASCADE, SET NULL, SET DEFAULT, RESTRICT and NO ACTION behaved as listed; a parent column without a UNIQUE index gives `foreign key mismatch`; `DEFERRABLE INITIALLY DEFERRED` defers the check to COMMIT (violation fails the commit); `RENAME` of a parent updated the child's REFERENCES with enforcement on and, with `foreign_keys=OFF` plus `legacy_alter_table=ON`, did not. The 3.26.0 release log adds `legacy_alter_table`; sqlite.org describes `SQLITE_DEFAULT_FOREIGN_KEYS` and the OMIT no-op case; Django's sqlite backend sets `foreign_keys`. The missing-index scan cost on parent delete was not measured.
