---
id: computing-software.data-engineering.data-warehouse-architecture.open-table-format-maintenance
name: open-table-format-maintenance
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, open-table-formats, table-maintenance, expire-snapshots, compaction, remove-orphan-files, rewrite-manifests, apache-iceberg, delta-lake, small-files]
level: practitioner
status: verified
description: "Keep Iceberg and Delta tables healthy: compaction, expiring snapshots, removing orphan files, rewriting manifests, and safe retention windows for readers and streams."
sources:
  - https://iceberg.apache.org/docs/latest/spark-procedures/
  - https://iceberg.apache.org/docs/latest/configuration/
  - https://docs.delta.io/latest/delta-batch.html
  - https://docs.delta.io/latest/delta-utility.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Open table format maintenance

**Goal:** stop lakehouse tables degrading into millions of small files and unbounded metadata, without deleting files that a reader still needs.

## 1. Why tables rot
- Streaming / frequent commits → many small data files and many snapshots.
- Merge-on-read deletes → delete files that every read must apply.
- Every snapshot keeps old files alive → storage grows; metadata files and manifests pile up → planning slows.
- Failed writes leave orphan files nobody references.

## 2. Iceberg procedures (Spark)
```sql
-- Procedure and argument names below checked against the Iceberg Spark procedures docs (not run: no Spark here)
-- 1. compact data files (bin-pack, or sort / zorder)
CALL lake.system.rewrite_data_files(table => 'sales.orders',
     strategy => 'sort', sort_order => 'customer_id',
     options => map('target-file-size-bytes','536870912','min-input-files','5'),
     where => 'ts >= TIMESTAMP ''2026-10-01''');
-- 2. fold delete files back into data
CALL lake.system.rewrite_position_delete_files(table => 'sales.orders');
-- 3. expire snapshots
CALL lake.system.expire_snapshots(table => 'sales.orders',
     older_than => TIMESTAMP '2026-10-09 00:00:00', retain_last => 20);
-- 4. orphan files (only files older than the window)
CALL lake.system.remove_orphan_files(table => 'sales.orders',
     older_than => TIMESTAMP '2026-10-13 00:00:00');
-- 5. manifests
CALL lake.system.rewrite_manifests('sales.orders');
```
Table properties that automate parts of it:
`write.metadata.delete-after-commit.enabled=true`, `write.metadata.previous-versions-max=50` (default 100), `history.expire.max-snapshot-age-ms` (default 5 days) and `history.expire.min-snapshots-to-keep` (default 1). `expire_snapshots` itself defaults to `older_than` = 5 days ago and `retain_last` = 1; `rewrite_data_files` defaults: `min-input-files` 5, `target-file-size-bytes` 512 MB, `partial-progress.enabled` false.
Order matters: compact → expire snapshots → remove orphans.

## 3. Delta equivalents
```sql
OPTIMIZE sales.orders WHERE order_date >= '2026-10-01';      -- compaction (liquid clustering if enabled)
VACUUM sales.orders RETAIN 168 HOURS;                        -- delete unreferenced files > 7 days old
ALTER TABLE sales.orders SET TBLPROPERTIES ('delta.logRetentionDuration'='interval 30 days',
                                            'delta.deletedFileRetentionDuration'='interval 7 days');
```
The two properties default to 30 days (log) and 7 days (deleted files); `VACUUM` is not triggered automatically in open-source Delta. Delta checkpoints and log cleanup run automatically; on Databricks UC managed tables predictive optimization can run OPTIMIZE/VACUUM for you.

## 4. Safety rules
- **Orphan removal window ≥ longest-running write.** A file written by an in-flight job is not yet referenced; `older_than` of a few minutes deletes live data. Keep ≥ 3 days (the `remove_orphan_files` default for `older_than`).
- Snapshot retention ≥ longest time-travel need **and** ≥ the lag of any streaming reader (a Flink/Spark incremental reader resuming from an expired snapshot fails).
- Run maintenance from one scheduler per table; concurrent compaction and heavy MERGE conflict — compact by partition ranges that writers are not touching, or enable partial-progress commits (`partial-progress.enabled`).
- Object store versioning/soft delete doubles storage of "deleted" files — set lifecycle rules accordingly.

## 5. Schedule
| Task | Typical cadence |
|---|---|
| Compaction | hourly-daily for streaming tables, after big loads for batch |
| Expire snapshots / VACUUM | daily |
| Orphan files | weekly |
| Rewrite manifests | weekly or when planning slows |

## Verify
- [ ] Average data file size (Iceberg `files` metadata table, Delta `DESCRIBE DETAIL`) is 128 MB-1 GB.
- [ ] Snapshot count stays bounded over a month.
- [ ] No reader or stream failed with missing files after a maintenance run.
