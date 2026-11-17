---
id: computing-software.data-engineering.data-warehouse-architecture.apache-iceberg-tables
name: apache-iceberg-tables
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, open-table-formats, apache-iceberg, partition-evolution, hidden-partitioning, iceberg-catalog, rest-catalog, snapshots, time-travel, spark-sql]
level: practitioner
status: verified
description: "Design Apache Iceberg tables: choosing a catalog (REST, Glue, Nessie, Polaris), hidden partitioning and partition evolution, snapshots, time travel, branches and tags."
sources:
  - https://iceberg.apache.org/spec/
  - https://iceberg.apache.org/docs/latest/branching/
  - https://iceberg.apache.org/docs/latest/spark-configuration/
  - https://iceberg.apache.org/docs/latest/spark-procedures/
  - https://py.iceberg.apache.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apache Iceberg tables

**Goal:** tables on object storage that many engines (Spark, Trino, Flink, Snowflake, BigQuery, Athena, DuckDB) read and write safely, with partitioning you can change later.

## 1. Pick the catalog first
The catalog stores the pointer to the current metadata file; atomic swap of that pointer is what makes commits safe.
| Catalog | Notes |
|---|---|
| REST catalog (Apache Polaris, Snowflake Open Catalog, Unity Catalog Iceberg REST, Lakekeeper, Gravitino) | engine-neutral, recommended default |
| AWS Glue | native for Athena/EMR; one Glue table per Iceberg table |
| Nessie | Git-like branches across many tables |
| Hive Metastore / JDBC | legacy or small setups |
| Hadoop (path-based) | needs a file system with atomic rename; the Iceberg docs say concurrent writes are not safe on local FS or S3 — avoid for concurrent writers |
Every engine must use the **same** catalog for a table, or commits will overwrite each other.

```properties
# Spark session config for a REST catalog
spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions
spark.sql.catalog.lake=org.apache.iceberg.spark.SparkCatalog
spark.sql.catalog.lake.type=rest
spark.sql.catalog.lake.uri=https://<catalog-host>/api/catalog
spark.sql.catalog.lake.warehouse=<warehouse-name>
```
Spark statements in this skill follow the Iceberg Spark docs (REST `type`, `uri`, `warehouse`; `CREATE TAG ... RETAIN n DAYS`, `spark.wap.branch`, `fast_forward`, `rollback_to_snapshot`, `VERSION AS OF`); none were run (no Spark here). Branch and tag creation plus snapshot/history metadata tables were reproduced in PyIceberg (`refs()` listed `main`, `etl_audit`, `eom`).

## 2. Hidden partitioning
```sql
CREATE TABLE lake.sales.orders (
  order_id BIGINT, customer_id BIGINT, amount DECIMAL(18,2), ts TIMESTAMP)
USING iceberg
PARTITIONED BY (days(ts), bucket(16, customer_id))
TBLPROPERTIES ('format-version'='2', 'write.target-file-size-bytes'='536870912');
```
Transforms: `years/months/days/hours(ts)`, `bucket(N, col)`, `truncate(W, col)`, identity. Queries filter on `ts` directly — no separate `dt` column for users to forget, and pruning still works.

## 3. Partition evolution
```sql
ALTER TABLE lake.sales.orders REPLACE PARTITION FIELD days(ts) WITH hours(ts);
ALTER TABLE lake.sales.orders ADD PARTITION FIELD bucket(32, order_id);
ALTER TABLE lake.sales.orders DROP PARTITION FIELD bucket(16, customer_id);
```
Metadata-only: old files keep the old spec, new writes use the new spec, queries prune both. Reproduced with PyIceberg 0.12 (`update_spec()` replacing `ts_day` with an hourly field, then appending): `inspect.files()` showed data files under spec ids 1 and 2 side by side, and no rewrite happened. No rewrite required (rewrite later with `rewrite_data_files` if you want uniform layout).
Schema evolution is likewise by column ID: add, drop, rename, reorder and widen types (`int→long`, `float→double`, decimal precision up with the same scale, per the spec's promotion table) without rewriting files.

## 4. Snapshots, time travel, branches
```sql
SELECT * FROM lake.sales.orders.snapshots;            -- metadata tables: snapshots, history, files, manifests, partitions
SELECT * FROM lake.sales.orders VERSION AS OF 4348761234;
SELECT * FROM lake.sales.orders TIMESTAMP AS OF '2026-10-01 00:00:00';
CALL lake.system.rollback_to_snapshot('sales.orders', 4348761234);
ALTER TABLE lake.sales.orders CREATE BRANCH etl_audit;   -- write-audit-publish
ALTER TABLE lake.sales.orders CREATE TAG eom_2026_09 RETAIN 365 DAYS;
```
Write-audit-publish: write to a branch (`spark.wap.branch`), validate, then `CALL lake.system.fast_forward('sales.orders', 'main', 'etl_audit')`.

## 5. Format version and deletes
- v2 (the default since Iceberg 1.4.0) adds row-level deletes (position/equality delete files) for merge-on-read `UPDATE/DELETE/MERGE`; set `write.delete.mode`, `write.update.mode`, `write.merge.mode` to `merge-on-read` for frequent small changes, `copy-on-write` for read-heavy tables.
- v3 (newer engines) adds deletion vectors, row lineage, variant and nanosecond timestamps (all listed in the spec's v3 changes; confirm the exact list in the spec) — check every reader supports it before upgrading.

## Verify
- [ ] All engines writing the table use one catalog.
- [ ] Queries filtering on the source column show partition pruning (files scanned in `EXPLAIN`/UI).
- [ ] A partition spec change did not rewrite data (`files` metadata table shows mixed `spec_id`).
- [ ] Snapshot expiry is scheduled (see table maintenance).
