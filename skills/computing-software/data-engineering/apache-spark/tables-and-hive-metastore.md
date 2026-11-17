---
id: computing-software.data-engineering.apache-spark.tables-and-hive-metastore
name: tables-and-hive-metastore
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-data-sources, hive-metastore, managed-vs-external-tables, spark-catalog, glue-catalog, msck-repair, refresh-table, enablehivesupport, create-table-using]
level: practitioner
status: docs-checked
description: "Manage Spark tables in a metastore: managed vs external tables, Hive metastore vs Glue, MSCK REPAIR/partition discovery, REFRESH TABLE for stale caches, and DROP semantics."
sources:
  - https://spark.apache.org/docs/latest/sql-data-sources-hive-tables.html
  - https://spark.apache.org/docs/latest/sql-ref-syntax-ddl-create-table-datasource.html
  - https://spark.apache.org/docs/latest/sql-ref-syntax-ddl-repair-table.html
  - https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-glue.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tables and the Hive metastore

**Goal:** register datasets as tables that every engine sees consistently, without accidentally deleting data on DROP.

## Managed vs external
| | Managed | External |
|---|---|---|
| Created by | `CREATE TABLE t (...) USING parquet` / `saveAsTable` with no path | `... LOCATION 's3://...'` / `.option("path", ...)` |
| Data lives | Warehouse dir (`spark.sql.warehouse.dir`) | Your path |

Shared lake data written by several tools should be external (or governed by a catalog such as Unity Catalog / Glue / Polaris that you control deliberately).

```sql
CREATE TABLE IF NOT EXISTS sales.orders (
  order_id STRING, amount DECIMAL(12,2), order_date DATE)
USING parquet
PARTITIONED BY (order_date)
LOCATION 's3://lake/sales/orders/';
```

## Metastore choices
- Hive metastore: `SparkSession.builder.enableHiveSupport()`; set `spark.sql.hive.metastore.version` (default 2.3.10) to match the server.
- AWS Glue Data Catalog on EMR: `hive.metastore.client.factory.class=com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory`.
- Table formats bring their own catalogs (Iceberg REST/Glue/Nessie catalogs, Delta in Unity Catalog).

## Partitions written outside Spark SQL
Files dropped into new `order_date=...` folders are invisible to a Hive-style table until registered:
```sql
MSCK REPAIR TABLE sales.orders;                -- scans all folders (slow for many partitions)
ALTER TABLE sales.orders ADD IF NOT EXISTS PARTITION (order_date='2026-10-15');   -- targeted, fast
MSCK REPAIR TABLE sales.orders SYNC PARTITIONS; -- SYNC = DROP + ADD PARTITIONS
```

## Stale metadata
Spark caches file listings and table metadata. After another job rewrites files:
```sql
REFRESH TABLE sales.orders;
```

## Gotchas
- State `USING <format>` explicitly (Hive-format tables are created with `CREATE [EXTERNAL] TABLE ... STORED AS`).
- If the Glue default database has no location URI, give `CREATE TABLE` a `LOCATION` or use another database (EMR Glue page).

## Verify
- [ ] `DESCRIBE TABLE EXTENDED sales.orders` shows the intended `Location`.
- [ ] `SHOW PARTITIONS` includes the newest partition after each load.

## Checked

2026-11-01. Confirmed against the Spark Hive-tables page (`enableHiveSupport`, `spark.sql.hive.metastore.version` default), REPAIR TABLE page (`ADD|DROP|SYNC PARTITIONS`, SYNC = DROP + ADD), CREATE TABLE (datasource and Hive format) pages (`LOCATION`, default location when omitted) and the EMR Glue page (client factory class, default-database LOCATION caveat). Removed: Derby note, thrift URI, 3.2+ version, DROP semantics, stale-file symptom, case-sensitivity and legacy-conf notes (not on the cited pages).

Method: documentation only; no commands were run.
