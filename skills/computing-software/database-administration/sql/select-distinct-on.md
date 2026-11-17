---
id: computing-software.database-administration.sql.select-distinct-on
name: select-distinct-on
category: computing-software
field: database-administration
product: sql
tags: [sql, select-distinct-on]
level: practitioner
status: docs-checked
description: "Use DISTINCT and PostgreSQL DISTINCT ON to take the first row per key."
sources: ["https://www.postgresql.org/docs/current/sql-select.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SELECT DISTINCT and DISTINCT ON semantics

- `SELECT DISTINCT a, b` dedupes whole output rows.
- `SELECT DISTINCT ON (k) k, ts, v FROM t ORDER BY k, ts DESC;` keeps the first row per `k` per the ORDER BY. The DISTINCT ON expressions must match the leftmost ORDER BY expressions.
- Without ORDER BY the "first row" of each set is unpredictable.
- Gotcha: DISTINCT ON is an extension of the SQL standard; the portable alternative is ROW_NUMBER() = 1.
- Self-check: add a deterministic tiebreaker to ORDER BY and rerun twice; output must not change.

## Checked

2026-11-02. Confirmed in the PostgreSQL SELECT page: DISTINCT ON keeps the first row of each set, must match the leftmost ORDER BY, unpredictable without ORDER BY, extension of the standard. Removed: the NULL-equality remark and the SQLite link.
Method: documentation only; no commands were run.
