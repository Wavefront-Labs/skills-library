---
id: computing-software.database-administration.sql.cte-materialized-hint
name: cte-materialized-hint
category: computing-software
field: database-administration
product: sql
tags: [sql, cte-materialized-hint]
level: advanced
status: docs-checked
description: "Control whether PostgreSQL and SQLite inline or materialise a CTE."
sources: ["https://www.postgresql.org/docs/current/queries-with.html", "https://www.postgresql.org/docs/current/sql-select.html", "https://www.sqlite.org/lang_with.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MATERIALIZED and NOT MATERIALIZED CTEs

- PostgreSQL: a non-recursive, side-effect-free WITH query used exactly once is folded into the parent query; `WITH x AS MATERIALIZED (...)` forces separate calculation, `NOT MATERIALIZED` forces merging.
- SQLite supports the MATERIALIZED and NOT MATERIALIZED hints from version 3.35.0.
- Use MATERIALIZED when the CTE is expensive and referenced several times; use NOT MATERIALIZED to let restrictions from the parent query push down.
- Self-check: compare EXPLAIN with and without the keyword.

## Checked

2026-11-02. Confirmed: folding rule for side-effect-free single-use WITH queries, MATERIALIZED and NOT MATERIALIZED effects (WITH queries and SELECT pages), SQLite 3.35.0 availability (WITH clause page). Removed: PostgreSQL version numbers and the pre-12 fence claim.
Method: documentation only; no commands were run.
