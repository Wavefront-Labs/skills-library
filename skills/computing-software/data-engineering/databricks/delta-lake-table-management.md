---
id: computing-software.data-engineering.databricks.delta-lake-table-management
name: delta-lake-table-management
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, delta-lake, delta-table, merge-into, upsert, optimize, z-order, liquid-clustering, cluster-by, vacuum, time-travel, restore, schema-evolution, mergeschema, unity-catalog, predictive-optimization, small-files, deletion-vectors, describe-history, lakehouse, spark-sql]
level: practitioner
status: docs-checked
description: "Maintain Delta tables on Databricks: MERGE upserts, OPTIMIZE with Z-ORDER or liquid clustering, VACUUM retention and time travel, schema evolution, and Unity Catalog naming."
sources:
  - https://docs.databricks.com/en/delta/index.html
  - https://docs.databricks.com/en/delta/merge.html
  - https://docs.databricks.com/en/delta/clustering.html
  - https://docs.databricks.com/en/sql/language-manual/delta-vacuum.html
  - https://docs.delta.io/latest/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delta Lake table management on Databricks — fast, recoverable, tidy

**Goal:** keep Delta tables correct under upserts, fast to query, cheap to store, and recoverable when something goes wrong.

## 1. Name and create tables in Unity Catalog
Unity Catalog uses `catalog.schema.table`. Prefer managed tables (UC controls the storage, enables predictive optimization) unless another engine must own the path.
```sql
CREATE TABLE prod.sales.orders (
  order_id BIGINT, customer_id BIGINT, status STRING,
  amount DECIMAL(18,2), updated_at TIMESTAMP, order_date DATE)
CLUSTER BY (order_date, customer_id);
```
Separate catalogs per environment (`dev`, `prod`) so the same code runs with a different catalog parameter.

## 2. Upsert with MERGE
```sql
MERGE INTO prod.sales.orders AS t
USING (SELECT * FROM staged_orders_deduped
       ) AS s  -- deduplicate to one row per order_id first
ON t.order_id = s.order_id
WHEN MATCHED AND s.updated_at > t.updated_at THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
WHEN NOT MATCHED BY SOURCE AND t.order_date >= current_date() - 7 THEN DELETE;  -- optional, scoped
```
- **Gotcha:** if two source rows match one target row, MERGE fails. Deduplicate the source first, as above.
- Add a partition/cluster-column predicate in the `ON` clause (e.g. `AND t.order_date >= '2026-10-01'`) when you know the batch's range — it prunes files and reduces conflicts between concurrent writers.
- `WHEN NOT MATCHED BY SOURCE` (Databricks SQL and Databricks Runtime 12.2 LTS and above) deletes rows absent from the source — always scope it, or you delete the whole table on a partial batch.

## 3. File layout: OPTIMIZE, Z-ORDER, liquid clustering
- Streaming and frequent small MERGEs create small files. `OPTIMIZE table` compacts them.
- Legacy: `OPTIMIZE t ZORDER BY (customer_id)` co-locates values for data skipping; liquid clustering replaces table partitioning and ZORDER.
- Preferred on current runtimes: **liquid clustering** (`CLUSTER BY` on create, or `ALTER TABLE t CLUSTER BY (col)`). `OPTIMIZE` clusters new data, and Databricks recommends liquid clustering for all new tables.
- Avoid over-partitioning: liquid clustering is the documented replacement for partitioning and ZORDER.
- **Predictive optimization** (UC managed tables, if enabled for the account/catalog) runs OPTIMIZE and VACUUM automatically; check before scheduling your own jobs to avoid double work.

## 4. VACUUM and time travel
- Old data files stay after updates so you can time travel:
```sql
DESCRIBE HISTORY prod.sales.orders;
SELECT * FROM prod.sales.orders VERSION AS OF 42;
SELECT * FROM prod.sales.orders TIMESTAMP AS OF '2026-10-13T00:00:00Z';
RESTORE TABLE prod.sales.orders TO VERSION AS OF 42;
```
- `VACUUM t` deletes unreferenced files older than the retention threshold — **default 7 days** (`delta.deletedFileRetentionDuration = 'interval 7 days'`). After vacuum, time travel to earlier versions fails.
- **Gotcha:** `VACUUM t RETAIN 0 HOURS` is blocked by a safety check unless you disable `spark.databricks.delta.retentionDurationCheck.enabled`. Don't: long-running jobs can have files they still need deleted.
- Log retention is separate: `delta.logRetentionDuration` (default 30 days) controls how far back history goes.
- Run `VACUUM t DRY RUN` first to see what would be deleted.

## 5. Schema evolution
- Writes with a different schema fail by default (schema enforcement) — a feature.
- Allow schema changes deliberately; see "Update table schemas with schema evolution" in the Delta docs for the options.
- Renames and drops need column mapping: `ALTER TABLE t SET TBLPROPERTIES ('delta.columnMapping.mode' = 'name')`.
- Type widening is controlled by the `delta.enableTypeWidening` table property (default false).

Related: computing-software.data-engineering.data-warehouse-architecture.medallion-layering and computing-software.data-engineering.apache-spark.shuffle-and-skew-tuning.

## Verify
- [ ] `DESCRIBE DETAIL` file counts and sizes give an average file size in the hundreds of MB, not KB.
- [ ] Re-running the same MERGE batch produces zero changed rows (`DESCRIBE HISTORY` operationMetrics).
- [ ] VACUUM retention is ≥ 7 days and longer than your longest-running reader or stream.
- [ ] A `RESTORE` to a previous version was tested on a dev copy.
- [ ] Tables are referenced by three-part names everywhere in jobs.

## Checked
2026-10-28. Confirmed against the Databricks clustering, VACUUM, table history, table properties and MERGE pages (7-day deletedFileRetentionDuration, 30-day logRetentionDuration, retentionDurationCheck.enabled, DRY RUN, WHEN NOT MATCHED BY SOURCE from 12.2 LTS, liquid clustering replaces partitioning and ZORDER, predictive optimization runs OPTIMIZE and VACUUM, columnMapping.mode name, enableTypeWidening default false, RESTORE, DESCRIBE HISTORY). Removed: the 1 GB default file size, the 1 TB and 1 GB partition thresholds, the mergeSchema and autoMerge options, overwriteSchema, the multiple-rows error text, QUALIFY, protocol-upgrade and corrupt-state claims.
Method: documentation only; no commands were run.
