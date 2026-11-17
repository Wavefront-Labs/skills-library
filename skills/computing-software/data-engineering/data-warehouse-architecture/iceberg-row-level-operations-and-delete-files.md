---
id: computing-software.data-engineering.data-warehouse-architecture.iceberg-row-level-operations-and-delete-files
name: iceberg-row-level-operations-and-delete-files
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, iceberg-delete-files, apache-iceberg, merge-on-read, copy-on-write]
level: advanced
status: verified
description: "Choose Iceberg copy-on-write vs merge-on-read for UPDATE, DELETE and MERGE: position, equality and deletion-vector deletes, write modes, compaction and reader impact."
sources:
  - https://iceberg.apache.org/docs/latest/configuration/
  - https://iceberg.apache.org/docs/latest/spark-procedures/
  - https://iceberg.apache.org/spec/
  - https://iceberg.apache.org/docs/latest/spark-queries/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Iceberg row-level operations and delete files

**Goal:** fast updates/deletes on Iceberg without degrading reads over time.

## Two strategies
- **Copy-on-write (COW)**: rewrite whole data files containing changed rows. Slow writes, fastest reads. Good for infrequent, large batch changes.
- **Merge-on-read (MOR)**: write small **delete files** (and new data files for updated rows); readers merge them at query time. Fast writes, reads degrade until compaction. Good for frequent small changes (CDC, GDPR deletes).

```sql
ALTER TABLE lake.db.orders SET TBLPROPERTIES (
  'write.delete.mode' = 'merge-on-read',
  'write.update.mode' = 'merge-on-read',
  'write.merge.mode'  = 'merge-on-read'
);
```
Requires format version 2+ (the three `write.*.mode` properties default to `copy-on-write`). Not run here: no Spark.

## Delete file types
- **Position deletes** (v2): file path + row position; written by Spark MOR operations; cheap to apply.
- **Equality deletes** (v2): "delete rows where id = X"; written by streaming upserts (Flink); expensive for readers (must compare against all data files in scope) until compacted.
- **Deletion vectors** (v3): compact bitmaps per data file, replacing position delete files; the spec allows at most one per data file in a snapshot, and a DV must replace earlier position deletes for that file.

## Maintenance (essential for MOR)
```sql
CALL lake.system.rewrite_data_files(table => 'db.orders', options => map('delete-file-threshold', '2'));   -- default threshold is effectively off (2147483647)
CALL lake.system.rewrite_position_delete_files(table => 'db.orders');
CALL lake.system.expire_snapshots(table => 'db.orders', older_than => TIMESTAMP '2026-10-11 00:00:00');
```
Schedule compaction by partition, prioritising partitions with many delete files (metadata tables in Spark: `lake.db.orders.delete_files`, `.data_files`, `.files`; the docs use `catalog.db.table.<metadata_table>`).

## Reader impact
- Every engine reading the table must support the delete file types present (equality deletes and v3 DVs are not universally supported).
- Query planning slows with many small delete files; monitor `delete_files` counts.

## Gotchas
- Flink upsert mode produces equality deletes continuously: compaction is not optional.
- Mixing writers with different modes is allowed but confusing; set properties at the table.

## Verify
After a batch of MOR updates, `SELECT count(*) FROM lake.db.orders.delete_files` grows; after compaction it drops and query time returns to baseline.
