---
id: computing-software.database-administration.sql.returning-clause
name: returning-clause
category: computing-software
field: database-administration
product: sql
tags: [sql, returning-clause]
level: practitioner
status: docs-checked
description: "Fetch generated values and changed rows with RETURNING."
sources: ["https://www.postgresql.org/docs/current/sql-insert.html", "https://www.sqlite.org/lang_returning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RETURNING on INSERT UPDATE DELETE

- `INSERT INTO t (n) VALUES ('a') RETURNING id;` PostgreSQL; SQLite supports RETURNING since 3.35.0.
- Current PostgreSQL accepts `RETURNING WITH (OLD AS o, NEW AS n) o.*, n.*` to return old and new values.
- Avoids a second SELECT.
- Self-check: the returned id matches a SELECT by natural key.

## Checked

2026-11-02. Confirmed: RETURNING on INSERT with the OLD/NEW syntax (PostgreSQL INSERT page); SQLite 3.35.0 support (SQLite RETURNING page). Removed: MariaDB, SQL Server, Oracle, the PostgreSQL 18 attribution and the currval race claim.
Method: documentation only; no commands were run.
