---
id: computing-software.database-administration.sql.refresh-materialized-view
name: refresh-materialized-view
category: computing-software
field: database-administration
product: sql
tags: [sql, refresh-materialized-view]
level: practitioner
status: docs-checked
description: "Refresh materialised views without blocking readers."
sources: ["https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html", "https://www.postgresql.org/docs/current/view-pg-matviews.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REFRESH MATERIALIZED VIEW CONCURRENTLY

- `REFRESH MATERIALIZED VIEW mv;` can block other connections that are trying to read the view; `REFRESH MATERIALIZED VIEW CONCURRENTLY mv;` is only allowed if the view has at least one UNIQUE index that uses only column names and covers all rows.
- `WITH NO DATA` leaves the view unpopulated.
- Self-check: `SELECT ispopulated FROM pg_matviews`.

## Checked

2026-11-02. Confirmed in the REFRESH MATERIALIZED VIEW page and the pg_matviews page: blocking readers, CONCURRENTLY unique-index requirement, WITH NO DATA, ispopulated column. Removed: slower/unpopulated claims for CONCURRENTLY, pg_cron advice, SQLite remark.
Method: documentation only; no commands were run.
