---
id: computing-software.database-administration.sql.advisory-locks
name: advisory-locks
category: computing-software
field: database-administration
product: sql
tags: [sql, advisory-locks]
level: advanced
status: docs-checked
description: "Serialise application work with PostgreSQL advisory locks."
sources: ["https://www.postgresql.org/docs/current/functions-admin.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Advisory locks for application-level mutexes

- `SELECT pg_try_advisory_lock(42);` returns false without waiting if the lock cannot be acquired; `pg_advisory_xact_lock(key)` takes a transaction-level lock; session-level locks are released by `pg_advisory_unlock` or at session end, even if the client disconnects.
- Choose a stable key space (hash of name) and document it.
- Self-check: a second session's try-lock returns false while the first holds.

## Checked

2026-11-02. Confirmed against the PostgreSQL docs page for system administration functions (advisory lock functions): try-lock returns false without waiting, xact variant, session-level release and release at session end. Removed: PgBouncer pooling advice and leader-election use (no page read states them).
Method: documentation only; no commands were run.
