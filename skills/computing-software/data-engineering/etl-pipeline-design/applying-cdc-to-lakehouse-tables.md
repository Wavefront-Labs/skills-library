---
id: computing-software.data-engineering.etl-pipeline-design.applying-cdc-to-lakehouse-tables
name: applying-cdc-to-lakehouse-tables
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, cdc-to-lakehouse, merge, delta-lake, apache-iceberg]
level: advanced
status: docs-checked
description: "Apply CDC streams (Debezium-style insert/update/delete events) to Delta or Iceberg tables: dedup per key, ordering, MERGE with deletes, SCD2 variants and compaction."
sources:
  - https://docs.databricks.com/aws/en/dlt/cdc
  - https://docs.delta.io/latest/delta-update.html#merge-examples
  - https://iceberg.apache.org/docs/latest/spark-writes/#merge-into
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Applying CDC to lakehouse tables

**Goal:** a Delta/Iceberg table that mirrors the source table exactly, updated from change events in batches.

## Event shape
Each change: key, operation (`c`/`u`/`d` or `I`/`U`/`D`), ordering field (LSN/SCN/binlog position or source commit timestamp + sequence), after-image (and before-image for deletes).

## Per batch: keep the last change per key
```sql
CREATE OR REPLACE TEMP VIEW changes AS
SELECT * FROM (
  SELECT *, row_number() OVER (PARTITION BY id ORDER BY source_lsn DESC) rn
  FROM bronze.orders_cdc WHERE _batch_id = :batch)
WHERE rn = 1;
```
Without this, MERGE can see several source rows for one target row, or apply changes out of order.

## MERGE with deletes
```sql
MERGE INTO silver.orders t
USING changes s ON t.id = s.id
WHEN MATCHED AND s.op = 'd' THEN DELETE
WHEN MATCHED AND s.source_lsn > t.source_lsn THEN UPDATE SET *
WHEN NOT MATCHED AND s.op <> 'd' THEN INSERT *;
```
The `source_lsn > t.source_lsn` guard makes replays and out-of-order batches safe.

## Managed alternatives
- Databricks Lakeflow: the `AUTO CDC` APIs (Python `create_auto_cdc_flow` with `keys`, `sequence_by`, `apply_as_deletes`, `stored_as_scd_type` of 1 or 2) apply CDC feeds ordered by the sequence column.
- Iceberg: Spark `MERGE INTO` (see the Iceberg Spark writes page).
- Delta streaming: `foreachBatch` running the MERGE above.

## SCD2 instead of mirror
Insert a new version per change, close the previous version (`valid_to = s.source_ts`), mark deletes with `is_deleted` rather than removing.

## Performance
- Partition or cluster the target on a column used in the ON clause so MERGE touches few files, and compact regularly.
- Snapshot load first (full copy), then apply changes from the snapshot's log position.

## Verify
Periodic full comparison of keys and row hashes between source and target shows zero differences.

## Checked

2026-10-28. Confirmed in the Databricks AUTO CDC page: `create_auto_cdc_flow` with `keys`, `sequence_by`, `apply_as_deletes` and `stored_as_scd_type` 1 or 2. Removed: the MERGE error text, liquid clustering, deletion vectors, merge-on-read and Flink equality-delete claims (not found in the cited pages). The SQL examples are illustrative table names.

Method: documentation only; no commands were run.
