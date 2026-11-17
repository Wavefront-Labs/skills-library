---
id: computing-software.database-administration.sql.expression-indexes
name: expression-indexes
category: computing-software
field: database-administration
product: sql
tags: [sql, expression-indexes]
level: practitioner
status: docs-checked
description: "Index computed values so function-based predicates stay indexable."
sources: ["https://www.postgresql.org/docs/current/indexes-expressional.html", "https://www.postgresql.org/docs/current/sql-createindex.html", "https://www.sqlite.org/expridx.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expression indexes

- `CREATE INDEX ON users (lower(email));` then query `WHERE lower(email) = $1` (PostgreSQL, SQLite).
- SQLite requires the query expression to be the same as the index expression, apart from minor syntactic differences such as white space; it does not do algebra.
- Functions and operators used in an index definition must be immutable (PostgreSQL).
- Self-check: EXPLAIN uses the index when the query uses the same expression.

## Checked

2026-11-02. Confirmed: expression index syntax and the immutable requirement (PostgreSQL expression index and CREATE INDEX pages); SQLite's same-expression matching rule (SQLite expression index page). Removed: the generated-column alternative and the seq-scan claim.
Method: documentation only; no commands were run.
