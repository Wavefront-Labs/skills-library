---
id: computing-software.cloud-infrastructure-engineering.aws.glue-athena-lake-formation-data-lake
name: glue-athena-lake-formation-data-lake
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, glue, athena, lake-formation, data-lake, glue-data-catalog, glue-crawler, glue-etl, glue-jobs, pyspark, parquet, partitioning, partition-projection, iceberg, athena-workgroups, ctas, msck-repair, lf-tags, fine-grained-access, s3-tables, data-lake-architecture]
level: practitioner
status: draft
description: "Build an S3 data lake on AWS: Glue Data Catalog and crawlers, Glue ETL writing partitioned Parquet or Iceberg, Athena workgroups and scan-cost control, and Lake Formation LF-tag permissions."
sources: ["AWS Glue Developer Guide - Data Catalog, crawlers and ETL jobs", "Amazon Athena User Guide - Partitioning, partition projection and performance tuning", "AWS Lake Formation Developer Guide - Lake Formation permissions and LF-tag based access control", "Amazon Athena User Guide - Using Apache Iceberg tables"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Glue, Athena and Lake Formation — a data lake that is cheap to query and safe to share

**Goal:** raw data lands in S3, Glue catalogues and transforms it into partitioned
columnar tables, Athena answers questions for cents, and Lake Formation decides who sees
which columns and rows.

## 1. Layout
```
s3://lake-raw/<source>/<table>/dt=2026-10-15/…        (as received; JSON/CSV; lifecycle to IA/Glacier)
s3://lake-curated/<domain>/<table>/dt=2026-10-15/…    (Parquet or Iceberg; the queryable layer)
s3://lake-athena-results/<workgroup>/…                 (query output; 7-day lifecycle)
```
- Zones: raw → curated (cleaned, typed, deduped) → optional marts. Separate buckets so
  Lake Formation/IAM can differ; SSE-KMS; bucket keys on.
- **Hive-style partitions** (`dt=`, `region=`) on the columns queries filter by; aim for
  files of 128 MB–1 GB; avoid > ~10 k partitions per table or use partition projection/Iceberg.
- Formats: **Parquet** (Snappy/ZSTD) for analytics; **Iceberg** when you need updates/deletes,
  time travel, schema evolution or hidden partitioning (Athena v3 + Glue support it natively;
  **S3 Tables** offer managed Iceberg with automatic compaction).

## 2. Glue Data Catalog and crawlers
- Catalog = Hive metastore for the account/region: databases, tables (schema, location,
  SerDe, partitions). Share across accounts via Lake Formation/RAM.
- **Crawlers** infer schema and add partitions: `aws glue start-crawler --name raw-orders`;
  schedule after each load; set `SchemaChangePolicy` (`UpdateInDatabase` vs `LOG`) and
  table-level grouping to avoid one table per prefix. For stable schemas, prefer **explicit
  DDL in IaC** + `ALTER TABLE ADD PARTITION` / partition projection — crawlers are slow and surprise you.
- Catalog table property for new partitions from pipelines: `glue:update-partition` from the
  job, or `MSCK REPAIR TABLE` (slow, scans the prefix) — use `ALTER TABLE … ADD PARTITION` instead.
- **Schema registry** for streaming (Avro/JSON/Protobuf) feeding Kinesis/MSK → Glue streaming jobs.

## 3. Glue ETL jobs
- **Spark jobs** (PySpark, Glue 4.x/5.x = Spark 3.x) with DynamicFrames or plain DataFrames:
  ```python
  df = spark.read.json("s3://lake-raw/shop/orders/dt=2026-10-15/")
  df.dropDuplicates(["order_id"]).write.mode("overwrite").partitionBy("dt").parquet("s3://lake-curated/shop/orders/")
  ```
  Use **job bookmarks** for incremental processing of new files; `--enable-auto-scaling`,
  workers `G.1X`/`G.2X` (Graviton `G.*` flex for cost); **Flex execution** for non-urgent jobs.
- **Python shell** jobs for light work; **Ray** jobs for Python-native scale; **Glue
  Studio** visual editor generates code (fine for simple maps).
- Glue **Data Quality** rules (`Rules = [ IsComplete "order_id", ColumnValues "status" in ["paid","refunded"] ]`)
  gate the curated write.
- Orchestrate with Glue **workflows/triggers** or Step Functions (`glue:startJobRun.sync`);
  alarm on `glue.driver.aggregate.numFailedTasks` and job `FAILED` events.
- Interactive dev: Glue **interactive sessions** (Jupyter) or notebooks; test locally with the `aws-glue-libs` Docker image.

## 4. Athena
- **Workgroups** per team: enforce result location, **per-query data scanned limit**
  (`bytesScannedCutoffPerQuery`), CloudWatch metrics, Athena engine v3, and tag for cost.
- Cost = $/TB scanned: columnar + partition pruning + `LIMIT` does not help without a
  `WHERE` on partitions. Check `EXPLAIN ANALYZE` / `Data scanned` on each query.
- **Partition projection** (table properties `projection.dt.type=date, projection.dt.range=2024-01-01,NOW, storage.location.template=s3://…/dt=${dt}`)
  removes catalog partition management for time-based data.
- **CTAS** / `INSERT INTO` to materialise Parquet from raw; `UNLOAD` to export.
- Iceberg DML: `MERGE INTO`, `UPDATE`, `DELETE`, `OPTIMIZE table REWRITE DATA USING BIN_PACK`, `VACUUM` for snapshot expiry.
- **Federated queries** (Lambda connectors) to RDS/DynamoDB/CloudWatch for joins without copying.
- Prepared statements and `--query-execution-context` for apps; results are files — consumers read S3 or use the pagination API.

## 5. Lake Formation
1. Register S3 locations with a Lake Formation service role; switch the catalog's default
   permissions from "IAM access control" (the legacy `IAMAllowedPrincipals` grant) to
   Lake Formation per database/table — do it per database as you migrate.
2. Grant with **LF-tags** (`Confidentiality=public|internal|pii`) assigned to databases/tables/columns;
   grant principals `SELECT` on `Confidentiality=internal` rather than table by table.
3. **Column-level** (exclude `email`) and **row-level** (data filter `region = 'EU'`) permissions on tables; **data cell filters** combine both.
4. Cross-account: grant to another account/OU via Lake Formation (uses RAM); the consumer
   creates a **resource link**. Athena/Redshift Spectrum/EMR/Glue honour LF permissions when
   the principal has no direct S3 access.
5. Audit via CloudTrail `GetDataAccess` events and the Lake Formation **data access** logs.

## Gotchas
- Lake Formation + IAM both apply: a user with `s3:GetObject` on the bucket bypasses LF; remove direct S3 access for analysts.
- Crawlers on raw JSON with evolving schemas create columns of type `struct` that later break on a changed field; land as string and cast in ETL, or use Iceberg schema evolution.
- Small files (Kinesis Firehose 60 s buffers) kill Athena performance: compact nightly (`CTAS` into bigger files or Iceberg `OPTIMIZE`).
- Athena `MSCK REPAIR` on a huge prefix times out; projection or explicit partitions.
- Glue job default 10 workers × G.1X billed per DPU-hour with a 1-minute minimum; a job stuck on a skewed partition burns money — set job timeout.
- Unconfirmed: current Glue version numbers and S3 Tables regional availability — check the docs.

## Verify
- [ ] Curated tables are Parquet/Iceberg, partitioned, files mostly > 100 MB (`aws s3 ls --summarize`).
- [ ] A typical analyst query scans < 1 % of the table (Athena "Data scanned") thanks to partition pruning.
- [ ] Workgroup enforces result location and a per-query scan cutoff; an over-limit query is cancelled.
- [ ] An analyst granted `Confidentiality=internal` cannot `SELECT email` from a PII-tagged column (error, not nulls).
- [ ] Glue job re-run with bookmarks processes only new files (row count delta matches).
