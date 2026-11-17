---
id: computing-software.database-administration.yugabytedb.colocated-tables-and-databases
name: colocated-tables-and-databases
category: computing-software
field: database-administration
product: yugabytedb
tags: [colocation, ysql, tablets, ysql-colocate-database-by-default, yb-table-properties, small-datasets]
level: practitioner
status: docs-checked
description: "Use YSQL colocation to put many small tables in one tablet, enable it per cluster, database or table, and check whether an object is colocated."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/additional-features/colocation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Colocated tables and databases

Colocation stores the tables of a database in a single parent tablet (the colocation tablet), still replicated by the cluster RF. It cuts per-tablet overhead and avoids network hops for joins on small tables.

Good fits: databases under about 50 GB with many tables and indexes that still need HA or geo-distribution; a few large tables beside many small ones (colocate the small ones, shard the large); and many small databases, such as one per microservice.

Enable it at three levels:
- Cluster: set `ysql_colocate_database_by_default = true` on both YB-Master and YB-TServer at cluster creation.
- Database: `CREATE DATABASE name WITH COLOCATION = true`
- Table opt-out inside a colocated database: `CREATE TABLE name (...) WITH (COLOCATION = false)`

You cannot create a colocated table in a non-colocated database. The older `colocated = true|false` syntax is deprecated since v2.18, and a database created with it cannot be upgraded in place; back it up and restore into a colocated cluster instead.

Check state with `SELECT yb_is_database_colocated();` and `SELECT is_colocated FROM yb_table_properties('table_name'::regclass);`. To move a table out of colocation, rename it, create a new table with CREATE TABLE AS SELECT, and switch applications over.

## Checked

2026-11-04. Confirmed against the colocation page: single colocation tablet still replicated by the cluster RF, the three use cases and the 50 GB guideline, the `ysql_colocate_database_by_default` flag on YB-Master and YB-TServer, `CREATE DATABASE ... WITH COLOCATION = true`, per-table `WITH (COLOCATION = false)`, no colocated table in a non-colocated database, the `colocated = <true|false>` syntax deprecated in v2.18 with no in-place upgrade (back up and restore into a colocated cluster), `yb_is_database_colocated()`, `yb_table_properties()` and the rename plus CREATE TABLE AS SELECT procedure. Nothing removed. The page also notes tablet splitting is disabled for colocated tables and that changing a table's colocation needs some downtime.

Method: documentation only; no commands were run.
