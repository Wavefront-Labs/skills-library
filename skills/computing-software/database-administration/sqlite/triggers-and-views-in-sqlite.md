---
id: computing-software.database-administration.sqlite.triggers-and-views-in-sqlite
name: triggers-and-views-in-sqlite
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-triggers, sqlite-views, instead-of-trigger, sqlite-schema, audit-trigger]
level: practitioner
status: verified
description: "Write SQLite triggers (BEFORE/AFTER, FOR EACH ROW, WHEN, RAISE) and views with INSTEAD OF triggers for audit columns, history tables and updatable views."
sources:
  - https://sqlite.org/lang_createtrigger.html
  - https://sqlite.org/lang_createview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Triggers and views in SQLite

## Audit timestamp trigger
```sql
CREATE TRIGGER orders_touch AFTER UPDATE ON orders
FOR EACH ROW WHEN NEW.updated_at IS OLD.updated_at
BEGIN
  UPDATE orders SET updated_at = strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE id = NEW.id;
END;
```
With `recursive_triggers` off (the default) the trigger's own UPDATE does not re-fire it: an unguarded `AFTER UPDATE` trigger that updates its own table ran once (3.50.4). The `WHEN` guard only helps once `PRAGMA recursive_triggers=ON`, and only while the new timestamp differs from the old one: with `%f` (millisecond) resolution an update within the same millisecond as the previous touch failed with `too many levels of trigger recursion`, while one 10 ms later worked. Keep the guard and do not turn recursion on for this pattern, or compare against a column the trigger does not rewrite.

## History table
```sql
CREATE TRIGGER orders_hist AFTER UPDATE OF status ON orders
BEGIN
  INSERT INTO order_status_history(order_id, old_status, new_status, changed_at)
  VALUES (OLD.id, OLD.status, NEW.status, strftime('%s','now'));
END;
```

## Validation with RAISE
```sql
CREATE TRIGGER stock_nonneg BEFORE UPDATE OF qty ON stock
WHEN NEW.qty < 0
BEGIN
  SELECT RAISE(ABORT, 'stock cannot go negative');
END;
```
`RAISE(IGNORE)` skips the row silently (tested: `UPDATE s2 SET qty=qty+10` left row 1 unchanged and changed row 2); `ROLLBACK`/`FAIL` have different transaction effects. `RAISE(ABORT, ...)` surfaced as `stock cannot go negative`. Prefer CHECK constraints when the rule involves only the row itself.

## Views and INSTEAD OF triggers
Views are read-only unless you add INSTEAD OF triggers (without one, `DELETE FROM active_users` failed with `cannot modify active_users because it is a view`; with the trigger below the user row got its `deleted_at` set):
```sql
CREATE VIEW active_users AS SELECT id, email FROM users WHERE deleted_at IS NULL;
CREATE TRIGGER active_users_del INSTEAD OF DELETE ON active_users
BEGIN
  UPDATE users SET deleted_at = datetime('now') WHERE id = OLD.id;
END;
```

## Limitations
- Only `FOR EACH ROW` (no statement-level triggers; `FOR EACH STATEMENT` is a syntax error).
- A non-TEMP trigger may only touch tables in its own database and the target table must be unqualified (`qualified table names are not allowed on INSERT, UPDATE, and DELETE statements within triggers`). A TEMP trigger may query or modify any attached database's table, again by unqualified name (tested: `CREATE TEMP TRIGGER ... ON main.r BEGIN INSERT INTO t ...` wrote into `aux.t`).
- No `CREATE OR REPLACE` (`near "or": syntax error`): `DROP TRIGGER IF EXISTS` then create.
- Triggers run inside the statement's transaction: slow trigger bodies slow every write.
- `.schema` shows triggers; `.eqp trigger` shows their bytecode (3.54.1 printed a `-- TRIGGER tr` program after the INSERT).

## Verify
Write a test that updates a row and asserts the history row exists and `updated_at` changed; check `SELECT name FROM sqlite_schema WHERE type='trigger'`.
