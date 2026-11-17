---
id: computing-software.database-administration.sql.on-conflict-do-update
name: on-conflict-do-update
category: computing-software
field: database-administration
product: sql
tags: [sql, on-conflict-do-update]
level: practitioner
status: docs-checked
description: "Upsert with ON CONFLICT using EXCLUDED and conflict targets."
sources: ["https://www.postgresql.org/docs/current/sql-insert.html", "https://www.sqlite.org/lang_upsert.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# INSERT ON CONFLICT DO UPDATE

- `INSERT INTO t (id, n) VALUES (1, 5) ON CONFLICT (id) DO UPDATE SET n = t.n + EXCLUDED.n;` (PostgreSQL; SQLite added UPSERT in 3.24.0).
- `DO NOTHING` skips duplicates; the target needs a unique index or constraint.
- Add `WHERE` to DO UPDATE to restrict which conflicting rows are updated.
- Self-check: run twice and confirm counts stay stable.

## Checked

2026-11-02. Confirmed: ON CONFLICT ... DO UPDATE / DO NOTHING and EXCLUDED in the PostgreSQL INSERT page; SQLite UPSERT added in 3.24.0 (SQLite upsert page). Removed: PostgreSQL 9.5, the second-time error message, and the MySQL syntax (no page read states them).
Method: documentation only; no commands were run.
