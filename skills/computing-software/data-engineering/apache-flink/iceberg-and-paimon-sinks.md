---
id: computing-software.data-engineering.apache-flink.iceberg-and-paimon-sinks
name: iceberg-and-paimon-sinks
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-iceberg-sink, apache-paimon, apache-iceberg, lakehouse, upsert, small-files]
level: advanced
status: docs-checked
description: "Stream from Flink into Apache Iceberg or Paimon tables: commit-on-checkpoint semantics, upsert/equality deletes, small-file compaction, and choosing between them."
sources:
  - https://iceberg.apache.org/docs/latest/flink-writes/
  - https://paimon.apache.org/docs/master/flink/sql-write/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Iceberg and Paimon sinks

Both commit data files atomically **on each Flink checkpoint** (two-phase: files written continuously, snapshot committed when the checkpoint completes). Data becomes visible to readers at checkpoint frequency, so the checkpoint interval is the freshness/small-file dial.

## Iceberg
```sql
CREATE TABLE lake.db.orders (
  order_id BIGINT, status STRING, amount DECIMAL(12,2), updated_at TIMESTAMP(3), dt STRING,
  PRIMARY KEY (order_id, dt) NOT ENFORCED
) PARTITIONED BY (dt) WITH ('format-version'='2', 'write.upsert.enabled'='true',
  'write.target-file-size-bytes'='134217728');
INSERT INTO lake.db.orders SELECT ... FROM orders_cdc;
```
- Append-only streams: plain inserts, simplest and fastest.
- CDC/upserts: format v2 with `write.upsert.enabled` writes **equality deletes** plus inserts. Readers must merge deletes; without regular compaction, read performance degrades quickly. The primary key must include the partition columns.
- Compaction is separate from writing: the Iceberg Flink docs describe a table-maintenance API (for example `rewriteDataFiles()` to compact small files); otherwise schedule compaction and snapshot expiry yourself.
- Avoid too many writers per partition: HASH distribution mode shuffles by partition key (or equality fields on unpartitioned tables) so each partition gets few files.
- One snapshot per checkpoint: 1-minute checkpoints = 1440 snapshots/day; expire them.

## Paimon
Designed for Flink streaming upserts: an LSM tree per bucket with **built-in compaction** and changelog generation.
```sql
CREATE TABLE paimon.db.orders (
  order_id BIGINT, status STRING, amount DECIMAL(12,2), updated_at TIMESTAMP(3), dt STRING,
  PRIMARY KEY (dt, order_id) NOT ENFORCED
) PARTITIONED BY (dt) WITH ('bucket'='8', 'merge-engine'='deduplicate', 'changelog-producer'='lookup');
```
- `merge-engine`: `deduplicate` (last wins), `partial-update` (merge columns from several streams by key), `aggregation`; see the Paimon merge-engine docs for the full list.
- `changelog-producer=lookup|full-compaction` lets downstream Flink jobs stream-read a complete changelog from the table.
- `bucket=-1` dynamic buckets for unknown key distributions.
- Compaction runs in the writer (can be moved to a dedicated job with `write-only=true` + `paimon-flink-action compact`).

## Choosing
- Many engines (Spark, Trino, Snowflake) reading and mostly append data: Iceberg.
- Heavy streaming upserts, partial updates, Flink-to-Flink streaming reads: Paimon (readable by Spark/Trino too, smaller ecosystem).

## Verify
- [ ] Table snapshots appear at each checkpoint; row counts match the source after a restart.
- [ ] Average file size per partition near target after compaction runs.

## Checked

2026-10-28. Confirmed: write.upsert.enabled, partition columns in the equality fields, HASH distribution and rewriteDataFiles maintenance on the Iceberg Flink page; write-only, paimon-flink-action compact and the lookup / full-compaction changelog producers on the Paimon pages. Removed: unconfirmed procedure and action names, version numbers, `sequence.field` and `first-row`.

Method: documentation only; no commands were run.
