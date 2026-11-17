---
id: computing-software.database-administration.sql.alter-table-safe-changes
name: alter-table-safe-changes
category: computing-software
field: database-administration
product: sql
tags: [sql, alter-table-safe-changes]
level: advanced
status: docs-checked
description: "Add columns, change types and add constraints in PostgreSQL with minimal locking, using NOT VALID, lock_timeout and CREATE INDEX CONCURRENTLY."
sources: ["https://www.postgresql.org/docs/current/sql-altertable.html", "https://www.postgresql.org/docs/current/runtime-config-client.html", "https://www.postgresql.org/docs/current/sql-createindex.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ALTER TABLE changes without long locks

- ALTER TABLE takes an ACCESS EXCLUSIVE lock unless the docs note otherwise.
- `ADD COLUMN` with a non-volatile `DEFAULT` needs no table rewrite. A volatile default, a stored generated column or an identity column rewrites the table and its indexes.
- Changing a column type normally rewrites the table and its indexes (binary-coercible changes are the exception).
- Add a foreign key, CHECK or not-null constraint with `NOT VALID`, then run `ALTER TABLE ... VALIDATE CONSTRAINT`; validation takes only a SHARE UPDATE EXCLUSIVE lock.
- Set `lock_timeout` (for example `SET lock_timeout = '3s'`) so a statement that waits longer than that for a lock aborts; 0, the default, disables it.
- `CREATE INDEX CONCURRENTLY` builds an index without locks that block concurrent inserts, updates or deletes. It does two scans, takes longer, and cannot run inside a transaction block.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
Read: the ALTER TABLE page's ADD COLUMN, ALTER COLUMN TYPE, ADD table_constraint, VALIDATE CONSTRAINT and Notes sections (searched and section-read, not read end to end); the lock_timeout entry on the client-defaults page; the CREATE INDEX CONCURRENTLY section.
Trimmed: the "PostgreSQL 11+" version claim (the page gives no version), the claim that DDL queues and blocks readers, and the pg_locks self-check. The SQLite source was dropped because no claim used it.
