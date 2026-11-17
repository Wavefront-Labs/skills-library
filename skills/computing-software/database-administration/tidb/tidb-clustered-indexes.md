---
id: computing-software.database-administration.tidb.tidb-clustered-indexes
name: tidb-clustered-indexes
category: computing-software
field: database-administration
product: tidb
tags: [tidb, clustered-index, nonclustered, primary-key, tidb-enable-clustered-index, tidb-rowid, index-organized-table]
level: practitioner
status: docs-checked
description: "Choose CLUSTERED or NONCLUSTERED primary keys in TiDB, set the default with tidb_enable_clustered_index, and know what can and cannot be changed afterward."
sources: ["https://docs.pingcap.com/tidb/stable/clustered-indexes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb clustered indexes

Since v5.0, TiDB tables with a primary key are either:
- `NONCLUSTERED`: row data is keyed by the internal `_tidb_rowid`, and the primary key is a separate unique index (primary key to `_tidb_rowid`). Two key-value pairs per row.
- `CLUSTERED`: row data is keyed directly by the primary key value, so one key-value pair per row (also called index-organized table). Only the `PRIMARY KEY` can be clustered.

Benefits of clustered: one fewer index write over the network on insert, and fewer index reads for queries by equality or range on the primary key or its prefix. Drawbacks: potential write hotspots when inserting many close-valued keys, and more storage if the key is wider than 64 bits, especially with many secondary indexes.

Syntax:

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) NONCLUSTERED);
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] CLUSTERED */, b VARCHAR(255));
```

Default when the keyword is omitted comes from `@@global.tidb_enable_clustered_index`: `ON` (default), `OFF`, or `INT_ONLY` (governed by `alter-primary-key`).

Limits: you cannot add or drop a clustered primary key after creation, nor convert between clustered and non-clustered. Non-clustered primary keys can be added or dropped with `ALTER TABLE`. Check with `SHOW CREATE TABLE`, `SHOW INDEX FROM`, or the `TIDB_PK_TYPE` column of `information_schema.tables`.

## Checked

2026-11-09. Confirmed the v5.0 introduction, key-value layout of both types, benefits and drawbacks, syntax forms including the TiDB comment form, the tidb_enable_clustered_index values and default, the add and drop limits and the three ways to check, against the PingCAP clustered indexes page (markdown source in the pingcap docs repository, read in full).

Method: docs-checked 2026-11-09 against the PingCAP docs page clustered-indexes.md
