---
id: computing-software.database-administration.sql.before-after-triggers
name: before-after-triggers
category: computing-software
field: database-administration
product: sql
tags: [sql, before-after-triggers]
level: practitioner
status: docs-checked
description: "Choose BEFORE or AFTER row triggers in PostgreSQL and know what the trigger function must return; notes the SQLite difference (row-level only)."
sources: ["https://www.postgresql.org/docs/current/sql-createtrigger.html", "https://www.postgresql.org/docs/current/plpgsql-trigger.html", "https://www.sqlite.org/lang_createtrigger.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BEFORE versus AFTER row triggers

- PostgreSQL: `CREATE TRIGGER trg BEFORE UPDATE ON t FOR EACH ROW EXECUTE FUNCTION f();`. Without FOR EACH ROW the default is FOR EACH STATEMENT.
- A BEFORE row trigger can skip the operation for that row or change the row (INSERT and UPDATE only). Returning NULL skips the row; for DELETE return `OLD`, since a returned `NEW` is null there.
- An AFTER trigger sees all changes, and its return value is ignored.
- SQLite supports only FOR EACH ROW triggers, not FOR EACH STATEMENT. Use `NEW.` and `OLD.` to reference columns, and a `WHEN` clause for a condition. If neither is given the trigger is a BEFORE trigger.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
Read: the CREATE TRIGGER pages for PostgreSQL (syntax, timing, FOR EACH ROW/STATEMENT) and SQLite (FOR EACH ROW only, NEW/OLD, WHEN, default timing), and the PL/pgSQL trigger-function return-value rules.
Added: the DELETE return rule. Trimmed: advice about cascading or recursive triggers and idempotence (not on the pages), and the self-check.
