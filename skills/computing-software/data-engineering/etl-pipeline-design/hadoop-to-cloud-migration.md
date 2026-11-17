---
id: computing-software.data-engineering.etl-pipeline-design.hadoop-to-cloud-migration
name: hadoop-to-cloud-migration
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, hadoop-migration, hive, hdfs, lakehouse-migration]
level: advanced
status: draft
description: "Migrate Hadoop (HDFS, Hive, Oozie, Spark on YARN) to cloud lakehouse or warehouse: data transfer, Hive metastore and table format conversion, jobs, security and cutover."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-distcp/DistCp.html
  - https://docs.databricks.com/aws/en/migration/
  - https://cloud.google.com/architecture/hadoop
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hadoop to cloud migration

**Goal:** retire an on-prem Hadoop cluster by moving data, metadata, jobs and access controls to a cloud platform with minimal downtime.

## Data
- Bulk copy with `hadoop distcp -update -delete -m 200 hdfs:///warehouse s3a://acme-lake/warehouse` (or cloud transfer appliances for petabytes); incremental `-update` passes until cutover.
- Verify with file counts and checksums (`-skipcrccheck` off when compatible; or compare row counts per partition after load).
- Bandwidth planning: TB/day achievable over the link decides the timeline.

## Metadata and formats
- Export Hive metastore table definitions (`SHOW CREATE TABLE`) or migrate the metastore DB; map to Glue/Unity Catalog/BigQuery/Snowflake external tables.
- Convert Hive tables (ORC/Parquet/text) to Delta or Iceberg: Delta `CONVERT TO DELTA parquet.\`path\` PARTITIONED BY (...)`; Iceberg `migrate`/`add_files` procedures; text/sequence files need rewrite.
- Fix small-file problems during conversion (compaction).

## Jobs
| Hadoop | Cloud target |
|---|---|
| Hive SQL | Spark SQL / Databricks SQL / warehouse SQL (translate with sqlglot) |
| Spark on YARN | Databricks/EMR/Dataproc Spark (mostly config changes: paths, `spark.yarn.*`) |
| MapReduce / Pig | rewrite in Spark or SQL |
| Oozie workflows | Airflow/Dagster/Databricks Jobs |
| Sqoop | managed CDC/EL tools or Spark JDBC |
| HBase | Bigtable/DynamoDB or Delta for analytical use |

## Security
Kerberos/Ranger/Sentry policies -> cloud IAM + catalog permissions (UC, Lake Formation). Export Ranger policies and map groups; review rather than copy blindly.

## Cutover
Run jobs on both platforms, compare outputs per partition, switch consumers domain by domain, freeze writes on Hadoop, final incremental copy, decommission.

## Gotchas
- Hive-specific semantics (implicit casts, `INSERT OVERWRITE` behaviour, case-insensitive columns, bucketing) differ across engines.
- Paths hard-coded in jobs (`hdfs://namenode:8020/...`).

## Verify
Per-table partition counts and row counts match; the same report produced on both platforms is identical for a full cycle.
