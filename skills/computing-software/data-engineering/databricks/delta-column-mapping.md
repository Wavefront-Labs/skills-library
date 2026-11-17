---
id: computing-software.data-engineering.databricks.delta-column-mapping
name: delta-column-mapping
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, delta-lake, column-mapping, rename-column, drop-column, schema-evolution, reader-writer-version, table-features, lakehouse-schema-change]
level: advanced
status: docs-checked
description: "Enable Delta column mapping to rename and drop columns without rewriting data, use special characters in names, and handle its protocol and streaming read impacts."
sources:
  - https://docs.databricks.com/en/delta/column-mapping.html
  - https://docs.delta.io/latest/delta-column-mapping.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Delta column mapping

**Goal:** rename or drop columns as metadata-only operations, instead of rewriting the table.

## Enable
```sql
ALTER TABLE sales.orders SET TBLPROPERTIES (
  'delta.columnMapping.mode' = 'name',
  'delta.minReaderVersion' = '2',
  'delta.minWriterVersion' = '5');
```
(Newer runtimes upgrade the protocol automatically when you set the mode.) Mode `name` maps logical column names to physical names in Parquet files.

## Operations it unlocks
```sql
ALTER TABLE sales.orders RENAME COLUMN cust_id TO customer_id;
ALTER TABLE sales.orders DROP COLUMN legacy_flag;
ALTER TABLE sales.orders DROP COLUMNS (tmp1, tmp2);
CREATE TABLE t (`order id` INT, `amount (usd)` DOUBLE) TBLPROPERTIES ('delta.columnMapping.mode' = 'name');
```
Without column mapping, column names cannot contain spaces or `,;{}()\n\t=`, and rename/drop require rewriting (`overwriteSchema`).

Dropped columns' data remains in files until they are rewritten (relevant for PII removal); look up the purge procedure in the Databricks docs.

## Compatibility impacts
- **Protocol upgrade is one-way** in practice (downgrade is possible with `DROP FEATURE` on Databricks Runtime 15.4 LTS and above, per the column mapping page). Older readers (old DBR, old OSS Delta, some external engines) cannot read the table.
- **Streaming reads:** after a rename/drop (non-additive change), streaming queries reading the table fail unless you use schema tracking:
```python
spark.readStream.option("schemaTrackingLocation", "/chk/orders_reader/_schema").table("sales.orders")
```
  plus the setting that acknowledges the non-additive change (see the Databricks streaming schema-tracking docs for its exact name).
- **Change data feed:** non-additive schema changes block CDF batch reads across the change boundary in some versions; read ranges on each side.
- External engines via UniForm/Iceberg handle column IDs well; plain Parquet readers see physical names (`col-<uuid>`), not logical ones.

## When to use
- Long-lived tables with evolving naming standards.
- PII column removal with purge.
- Ingesting sources whose column names contain spaces/special characters.

## Verify
- [ ] `DESCRIBE DETAIL` shows `minReaderVersion`/features include column mapping.
- [ ] Downstream streaming jobs restarted with schema tracking and process past the rename.

## Checked

2026-10-28. Confirmed: DROP FEATURE on DBR 15.4 LTS and above and minWriterVersion 5 on the column mapping pages. Removed: an unconfirmed streaming setting name and an unconfirmed REORG purge command.

Method: documentation only; no commands were run.
