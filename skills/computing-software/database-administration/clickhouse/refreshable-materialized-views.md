---
id: computing-software.database-administration.clickhouse.refreshable-materialized-views
name: refreshable-materialized-views
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, refreshable, materialized-view, refresh-every, systemview-refreshes]
level: practitioner
status: docs-checked
description: "Use refreshable materialized views for periodic full rebuilds, forcing refresh and checking system.view_refreshes."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/materialized-view/refreshable-materialized-view.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# refreshable materialized views
A refreshable materialized view recomputes its query on a schedule and writes the result to a target table, unlike incremental views that react to each insert. Use it for denormalisation, joins that cannot be incremental, or batch reports that tolerate staleness.
```sql
CREATE MATERIALIZED VIEW table_name_mv
REFRESH EVERY 1 MINUTE TO table_name AS
SELECT ... ;

SYSTEM REFRESH VIEW table_name_mv;                 -- force a run
ALTER TABLE table_name_mv MODIFY REFRESH EVERY 30 SECONDS;
```
You can also cancel, stop or start a view with `SYSTEM` commands. Views can depend on each other so one runs only after another completes.

Check state:
```sql
SELECT database, view, status, last_success_time, last_refresh_time,
       next_refresh_time, read_rows, written_rows
FROM system.view_refreshes;
```
Gotcha: each refresh rereads the full source, so cost scales with data size; for single-table aggregates the docs say incremental views scale much better. 
## Checked
2026-11-03. Confirmed against the ClickHouse docs page "Refreshable materialized view": REFRESH EVERY ... TO syntax, SYSTEM REFRESH VIEW, MODIFY REFRESH, dependencies, `system.view_refreshes` columns and the incremental-versus-refreshable guidance. Removed: the status-value Verify claim.
Method: documentation only; no commands were run.
