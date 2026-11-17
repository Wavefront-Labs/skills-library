---
id: computing-software.database-administration.yugabytedb.tablet-presplitting
name: tablet-presplitting
category: computing-software
field: database-administration
product: yugabytedb
tags: [tablet-splitting, presplit, split-into-tablets, split-at-values, range-sharding, hash-sharding]
level: practitioner
status: docs-checked
description: "Presplit YugabyteDB tables at creation with SPLIT INTO n TABLETS for hash tables or SPLIT AT VALUES for range tables, plus the default tablet counts and limits."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb-sharding/tablet-splitting.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/yb-master.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/yb-tserver.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Presplitting tablets

Presplitting divides a table into the desired number of tablets at creation time, before data is added. It is supported for range-sharded and hash-sharded YSQL tables and hash-sharded YCQL tables. The count can be given as a total, or as tablets per node, in which case the total is num_tablets_per_node * num_nodes_at_table_creation_time.

Hash-sharded tables:
```
CREATE TABLE t (k INT PRIMARY KEY, v TEXT) SPLIT INTO 16 TABLETS;
```
The same clause exists for CREATE INDEX; YCQL uses `CREATE TABLE ... WITH tablets`. Hash sharding applies a hash function to the key columns, so the byte space is known ahead of time (for a 2-byte hash, 0x0000 to 0xFFFF) and can be divided into the requested number of shards.

Range-sharded tables list the boundaries:
```
CREATE TABLE t (k INT, v TEXT, PRIMARY KEY (k ASC)) SPLIT AT VALUES ((1000), (2000), (3000));
```
Range-sharded YSQL tables must list split points explicitly, because each tablet's start and end key depend on the column type and intended usage, which the database cannot infer.

Defaults when you do not presplit:
- with automatic splitting on, a new hash-sharded table gets one tablet per node by default; from 2.14.10, servers with up to 2 CPU cores give one tablet per cluster and up to 4 cores give 2 tablets per cluster
- a new range-sharded table always gets one tablet per cluster unless partitioning is given explicitly at creation

Cautions:
- `max_create_tablets_per_ts` (default 50 in the yb-master reference) caps the tablets per tablet server allowed at table creation and also limits tablets created by splitting.
- The page warns, for manual splitting, that tablet merging is not currently supported, so extra tablets cannot easily be undone.
- The page's manual-split example creates a table with `SPLIT INTO 1 TABLETS`, so a single tablet is a valid request.

## Checked

2026-11-04. Confirmed against the Tablet splitting page (presplit support by table type, total versus per-node count, hash byte space, SPLIT INTO and SPLIT AT VALUES examples, default tablet counts, max_create_tablets_per_ts) and the yb-master and yb-tserver references (max_create_tablets_per_ts default 50, ysql_num_shards_per_tserver behaviour). Removed: the claim that bulk loads spread from the first write, the advice on choosing boundaries, the replica memory and CPU caution with its reference to another skill, and the claim that presplit tables keep splitting automatically, none of which the cited pages state.

Method: documentation only; no commands were run.
