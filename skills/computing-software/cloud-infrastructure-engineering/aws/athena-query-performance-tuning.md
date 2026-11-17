---
id: computing-software.cloud-infrastructure-engineering.aws.athena-query-performance-tuning
name: athena-query-performance-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, athena, athena-performance, predicate-pushdown, columnar-formats, file-sizing, query-optimization]
level: advanced
status: docs-checked
description: "Make Athena queries faster and cheaper: columnar formats and compression, file sizes, partition pruning, predicate pushdown, join order, approximate functions and result reuse."
sources: ["https://docs.aws.amazon.com/athena/latest/ug/performance-tuning.html", "https://docs.aws.amazon.com/athena/latest/ug/performance-tuning-data-optimization-techniques.html", "https://docs.aws.amazon.com/athena/latest/ug/reusing-query-results.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Athena query performance tuning

Less data scanned means faster queries; see the Athena pricing page for how queries are billed.

## 1. Data layout first
- **Columnar formats**: Parquet or ORC with compression. A query selecting 3
  of 50 columns reads only those columns. Convert raw JSON/CSV with a CTAS or INSERT INTO query (see the Athena CTAS documentation for the table properties).
- **File sizes**: prefer fewer, larger files. Thousands of tiny files (Firehose with small
  buffers, per-minute writers) make S3 listing and opening dominate query time; compact
  them (CTAS/INSERT, Glue job, or an Iceberg table compaction).
- **Partitioning** on columns used in WHERE (date, region, tenant) with partition
  projection to avoid catalogue lookups for many partitions. Do not over-partition into
  tiny files.
- **Sorting/bucketing**: sort by frequently filtered columns within files so Parquet
  min/max statistics skip row groups; Iceberg tables support sort orders.

## 2. Query patterns
- Filter on partition columns with literals (`WHERE dt BETWEEN '2026-10-01' AND
  '2026-10-07'`); functions on the partition column (`date(dt) = ...`) can prevent pruning.
- Select only needed columns; avoid `SELECT *` on wide tables.
- Joins: filter both sides before joining and check the join order in `EXPLAIN`.
- `ORDER BY` with `LIMIT` instead of ordering everything; avoid global ORDER BY on huge
  results.
- Use approximate aggregate functions where exactness is not required.
- `GROUP BY` high-cardinality columns last; push filters into subqueries/CTEs.
- Regular expressions and `LIKE '%x%'` on large text are expensive; pre-extract fields.

## 3. Engine features
- **Query result reuse**: re-running an identical query within a max age returns cached
  results without scanning (`ResultReuseConfiguration` / console toggle; the maximum age you can set is the equivalent of 7 days).
- `EXPLAIN` shows the plan and which partitions a query will scan.
- Query stats: `aws athena get-query-runtime-statistics --query-execution-id <id>` returns
  runtime statistics for the query execution.

## 4. Cost guardrails
Workgroup per team with `BytesScannedCutoffPerQuery`, workgroup CloudWatch metrics
(`PublishCloudWatchMetricsEnabled`) for budgets, and `EnforceWorkGroupConfiguration` so users cannot override.

## Verify
- [ ] Hot tables are Parquet/ORC and compacted (no swarm of tiny files).
- [ ] `EXPLAIN` of key queries shows partition pruning.
- [ ] Workgroup scan limits set; data scanned per query trending down.

## Checked

2026-10-28

Confirmed: partition projection, EXPLAIN for partition scan, LIMIT without ORDER BY not cached, 7-day maximum reuse age (Athena User Guide pages); ResultReuseConfiguration, BytesScannedCutoffPerQuery, EnforceWorkGroupConfiguration, PublishCloudWatchMetricsEnabled (botocore); get-query-runtime-statistics and its flag (check_commands).

Removed: price per TB claim, engine v3/Trino claim, 128 MB-1 GB file size, CTAS example with compression and location properties, join-order rule, named approximate functions, provisioned capacity, EXPLAIN ANALYZE, ProcessedBytes metric, Iceberg OPTIMIZE syntax.

Method: documentation only; no commands were run.
