---
id: computing-software.database-administration.yugabytedb.ddl-concurrency-and-ci-practices
name: ddl-concurrency-and-ci-practices
category: computing-software
field: database-administration
product: yugabytedb
tags: [best-practices, ddl, catalog-version, ci-testing, durable-wal-write, ysql]
level: practitioner
status: docs-checked
description: "Operational best practices: run DDL sequentially per database, expect catalog version retries, and configure single-AZ clusters and CI test clusters correctly."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/best-practices-operations/administration.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/yb-tserver.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DDL concurrency and CI practices

DDL can run concurrently with DML, but a schema or catalog version change makes in-flight statements fail with a mismatch error. Clients should retry them.

Rules for administrators:
- Run DDL on the same database sequentially, one statement at a time.
- Run DDL on shared objects (roles, tablespaces) sequentially across the whole cluster.
- Consider the YSQL catalog cache preload settings: cache misses are loaded from the YB-Master leader, so first queries on a new backend can be slow, especially if the master leader is in another region.
- Avoid running DML on a table while an ALTER TABLE that copies the whole table is modifying it; the DML effects may not reach the copy.
- Single-AZ clusters should set the yb-tserver flag `--durable_wal_write=true` (default false), so no data is lost if the whole data center goes down, for example in a power failure. The default is recommended only where AZs or regions are independent failure domains.

For CI or test clusters, the documented speed-ups are:
- point `--fs_data_dirs` and `--fs_wal_dirs` at a RAMDisk directory
- `--yb_num_shards_per_tserver=1`
- colocated databases
- `--replication_factor=1`
- clean state between tests with TRUNCATE instead of recreating tables

Do not carry these settings into production. `yb-admin ysql_catalog_version` prints the current YSQL catalog version, which helps when diagnosing mismatch errors.

## Checked

2026-11-04. Confirmed against the YSQL administrator best-practices page (concurrent DML during DDL and retry advice, sequential DDL per database and for shared objects, catalog cache preloading, CI settings: RAMDisk for `--fs_data_dirs` and `--fs_wal_dirs`, `--yb_num_shards_per_tserver=1`, colocation, `--replication_factor=1`, TRUNCATE), the yb-tserver reference (`--durable_wal_write` default false, set true for single AZ) and the yb-admin reference (`ysql_catalog_version`). Removed the `SELECT yb_catalog_version();` function, which no fetched page documents, and reworded the durability reason to the pages' wording.

Method: documentation only; no commands were run.
