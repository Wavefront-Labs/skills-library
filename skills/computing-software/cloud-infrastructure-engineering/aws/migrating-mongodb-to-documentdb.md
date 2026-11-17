---
id: computing-software.cloud-infrastructure-engineering.aws.migrating-mongodb-to-documentdb
name: migrating-mongodb-to-documentdb
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, documentdb, mongodb-migration, dms, compatibility-tool, change-streams, cutover]
level: advanced
status: draft
description: "Migrate MongoDB to Amazon DocumentDB: compatibility assessment, index migration, offline vs online (DMS CDC or change streams) methods, validation and cutover."
sources: ["https://docs.aws.amazon.com/documentdb/latest/developerguide/docdb-migration.html", "https://docs.aws.amazon.com/documentdb/latest/developerguide/functional-differences.html", "https://github.com/awslabs/amazon-documentdb-tools", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.DocumentDB.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migrating MongoDB to DocumentDB

## 1. Assess compatibility first
DocumentDB implements the MongoDB API (versions 4.0/5.0/8.0 compatibility) on its own
storage engine; not every operator, aggregation stage or index type exists.
- Run the **compatibility tool** from `amazon-documentdb-tools` against MongoDB logs or
  application source to list unsupported operators:
  `python3 compat.py --version 5.0 --directory ./app-src`
- Known gaps to check: some aggregation stages/operators, `$where`/server-side JavaScript,
  certain index types (text indexes have limits, geospatial support differs), capped
  collections, multi-document transaction limits, collation support, sharding model
  (use DocumentDB elastic clusters for sharded workloads).
- Note behaviour differences: default `retryWrites` must be **false** in connection strings
  for instance-based clusters (`retryWrites=false`), TLS on by default with the RDS CA.

## 2. Choose a method
| Method | Downtime | Use when |
|---|---|---|
| Offline: `mongodump`/`mongorestore` | full write freeze for the copy | small datasets, maintenance window available |
| Online: **DMS** full load + CDC (source MongoDB as DMS source, oplog-based) | minutes at cutover | most production moves |
| Hybrid: dump/restore then DMS CDC from a timestamp | minutes | large datasets where DMS full load is slow |
| Change-stream based tools (e.g. the DocumentDB tools' migrator) | minutes | DMS limitations |

## 3. Indexes before data
Migrate indexes first with the **index tool**:
```bash
python3 documentdb_index_tool.py --dump-indexes --uri "$SRC" --dir idx/
python3 documentdb_index_tool.py --show-issues --dir idx/      # unsupported index options
python3 documentdb_index_tool.py --restore-indexes --uri "$DST" --dir idx/
```
Building indexes before the load is slower to load but avoids long index builds after.

## 4. Online with DMS
- Source MongoDB must be a replica set (oplog). DMS endpoint `mongodb` with
  `NestingLevel=one` (document mode) to keep documents as-is.
- Target endpoint `docdb`, TLS with the CA bundle.
- Task: full load + CDC; tune `ParallelLoadThreads` / segmented loads by `_id` ranges for
  large collections.
- Monitor `CDCLatencySource`/`CDCLatencyTarget`; wait until near zero before cutover.

## 5. Size the target
Instance class by working set (indexes + hot data in memory: aim for the working set to
fit in buffer cache), storage auto-grows. Check `BufferCacheHitRatio` after load
(> 95% desired), `DatabaseConnections` vs instance limits.

## 6. Validate and cut over
- Counts per collection, sample document comparisons (DMS validation does not support
  MongoDB fully; script `countDocuments` and checksum samples).
- Run application integration tests against DocumentDB (read preference
  `secondaryPreferred` for reads to replicas, replica set name `rs0`).
- Cutover: stop writes, let CDC drain, switch connection strings, keep source read-only
  for rollback.

## Verify
- [ ] Compatibility report clean or each gap remediated in code.
- [ ] Indexes present on target before load; counts match after full load.
- [ ] CDC latency near zero before cutover; app passes tests against the target.
