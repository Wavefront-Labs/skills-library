---
id: computing-software.database-administration.yugabytedb.cluster-wide-and-tablet-metadata-views
name: cluster-wide-and-tablet-metadata-views
category: computing-software
field: database-administration
product: yugabytedb
tags: [gv-views, yb-enable-global-views, pg-read-all-stats, yb-local-tablets, yb-tablet-metadata, tablet-state, monitoring]
level: practitioner
status: docs-checked
description: "Query cluster-wide gv$ views with yb_enable_global_views and inspect tablets with yb_local_tablets and yb_tablet_metadata, including the tablet states."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/launch-and-manage/monitor-and-alert/cluster-wide-db-views.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/launch-and-manage/monitor-and-alert/tablet-metadata.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cluster-wide and tablet metadata views

**gv$ views** (v2026.1.2 or later) are foreign tables over an internal `yb_global_views_server` and return the rows of the per-node view from every node, with a `server_uuid` column. Examples: `gv$pg_stat_activity`, `gv$pg_stat_statements`, `gv$yb_active_session_history`, `gv$pg_stat_database`.
- Enable with the tserver flag `--ysql_pg_conf_csv=yb_enable_global_views=true` (default false).
- The querying role needs `pg_read_all_stats`.
- Use `server_uuid` to join to `yb_servers()` to identify the node.

**Tablet views:**
- `yb_local_tablets` returns tablets (YSQL, YCQL and system) on the node you are connected to; it matches the tserver UI `/tablets` page. Columns include `tablet_id`, `table_id`, `table_type`, `namespace_name`, `table_name`, `partition_key_start`, `partition_key_end` and `state`.
- `yb_tablet_metadata` gives placement and roles for the whole cluster (YSQL objects and the transaction table): `tablet_id`, `db_name`, `relname`, `start_hash_code`, `end_hash_code`, `leader`, `replicas`, `start_range`, `end_range`. `relname` and the range columns are masked unless you are superuser or have `yb_db_admin`.

Tablet states you may see: TABLET_DATA_COPYING (remote bootstrap in progress), TABLET_DATA_READY, TABLET_DATA_DELETED, TABLET_DATA_TOMBSTONED (replica removed from this node but the tablet still exists elsewhere), TABLET_DATA_SPLIT_COMPLETED and TABLET_DATA_INIT_STARTED (a child created by a split).

## Checked

2026-11-04. Confirmed against the cluster-wide database views and tablet metadata pages: gv$ views availability (v2026.1.2 and later), the yb_global_views_server foreign server, the yb_enable_global_views parameter (default false) and its --ysql_pg_conf_csv form, pg_read_all_stats, the yb_local_tablets and yb_tablet_metadata scope and masking rules, and the tablet states. Removed the generic use-case list.

Method: documentation only; no commands were run.
