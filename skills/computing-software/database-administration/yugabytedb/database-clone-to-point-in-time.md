---
id: computing-software.database-administration.yugabytedb.database-clone-to-point-in-time
name: database-clone-to-point-in-time
category: computing-software
field: database-administration
product: yugabytedb
tags: [clone, clone-database, clone-namespace, as-of, yb-database-clones, pitr, ysql-clone-pg-schema-rpc-timeout-ms]
level: advanced
status: docs-checked
description: "Create a zero-copy clone of a database as of a recent time with CREATE DATABASE TEMPLATE AS OF or yb-admin clone_namespace, and track clone status."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/backup-restore/point-in-time-recovery/clone.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Clone a database to a point in time

A clone is an independent writable copy that shares data files with the source, so it is quick and initially uses little extra disk. It always lives on the same cluster as the source. Prerequisite: a snapshot schedule on the database; the retention period of that schedule sets how far back you can clone. The requested time must fall inside the history retention window.

YSQL:
```
CREATE DATABASE clone_db TEMPLATE original_db;
CREATE DATABASE clone_db TEMPLATE original_db AS OF 1723146703674480;
CREATE DATABASE clone_db TEMPLATE original_db AS OF '2024-08-08 19:51:43.674480';
```
The AS OF value is a Unix timestamp in microseconds or a quoted PostgreSQL timestamp. An OWNER clause sets the owner; otherwise the current user owns the clone. With `yb-admin clone_namespace` the clone keeps the template database's owner. Cloning a database not marked datistemplate needs superuser or ownership of the source. Two clones of the same source cannot run at the same time.

YCQL:
```
yb-admin --master_addresses $MASTERS clone_namespace ycql.originaldb1 clonedb2 1715275616599020
yb-admin --master_addresses $MASTERS list_clones <source_namespace_id>
```
Check YSQL progress with `yb_database_clones()`.

Typical use: recover a dropped table while keeping later writes. Clone as of the good time, export the rows from the clone with COPY, and load them into production.

Limits:
- A clone as of a time close to the end of retention can fail; keep a margin.
- A clone creates an independent set of logical tablets, and the added tablet count can cause resource problems.
- Compaction on either side can increase disk use, since both versions of files must be kept.
- Cloning to a time during which DDL was running may fail, and databases with vector indexes cannot be cloned.
- A clone can exceed configured tablet limits (the operation does not respect them).
- Databases with many objects in multi-region deployments can take longer to clone; if it exceeds 10 minutes, raise the YB-TServer runtime flag `ysql_clone_pg_schema_rpc_timeout_ms`.

## Checked

2026-11-04. Confirmed against the Clone to PIT page: zero-copy shared files, same-cluster clones, snapshot schedule prerequisite, CREATE DATABASE ... TEMPLATE [AS OF] with microsecond or quoted timestamp, OWNER rules, `yb-admin clone_namespace ycql.originaldb1 clonedb2 <timestamp>`, `list_clones`, `yb_database_clones()`, the table-drop recovery use case, and the limits (retention margin, extra tablets, compaction disk use, 10 minute multi-region timeout and `ysql_clone_pg_schema_rpc_timeout_ms`). Added the page's additional limits (running DDL, vector indexes, tablet limits, one clone at a time per source).

Method: documentation only; no commands were run.
