---
id: computing-software.cloud-infrastructure-engineering.aws.redshift-warehousing-spectrum-wlm
name: redshift-warehousing-spectrum-wlm
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, redshift, redshift-spectrum, redshift-serverless, ra3, workload-management, wlm, auto-wlm, query-queues, concurrency-scaling, distribution-key, sort-key, distkey, sortkey, copy-command, unload, vacuum, analyze, data-warehouse, external-schema, glue-data-catalog, materialized-views, zero-etl, data-sharing, redshift-managed-storage, columnar, stl-tables, svl-query-report]
level: advanced
status: docs-checked
description: "Run Amazon Redshift: provisioned vs Serverless, dist/sort key design, COPY/UNLOAD, VACUUM/ANALYZE, Spectrum over S3, Auto WLM queues, QMR, concurrency scaling and data sharing."
sources: ["https://docs.aws.amazon.com/redshift/latest/dg/c_designing-tables-best-practices.html", "https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-best-dist-key.html", "https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-sort-key.html", "https://docs.aws.amazon.com/redshift/latest/dg/t_Defining_constraints.html", "https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-use-multiple-files.html", "https://docs.aws.amazon.com/redshift/latest/dg/r_MERGE.html", "https://docs.aws.amazon.com/redshift/latest/dg/c-spectrum-external-performance.html", "https://docs.aws.amazon.com/redshift/latest/dg/concurrency-scaling.html", "https://docs.aws.amazon.com/redshift/latest/dg/wlm-short-query-acceleration.html", "https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_TABLE_INFO.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-capacity.html", "https://docs.aws.amazon.com/redshift/latest/dg/datashare-overview.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redshift: warehousing, Spectrum and workload management

**Goal:** a warehouse where the big fact tables are distributed and sorted for the joins that actually run,
loads use `COPY` from S3 in parallel, cold history lives in S3 behind Spectrum, and WLM and concurrency scaling
keep dashboards fast while ETL runs, without a growing VACUUM backlog.

## 1. Provisioned vs Serverless
- **RA3** nodes (`ra3.large`, `ra3.xlplus`, `ra3.4xlarge`, `ra3.16xlarge`) and the newer RG type use
  **Redshift Managed Storage**; you pay for storage separately from nodes. Elastic resize averages about ten
  minutes. See the RA3 skill for sizing. Pick provisioned when load is steady and predictable.
- **Serverless**: workgroup (compute, in RPUs) plus namespace (data, users). Base capacity is 4 to 512 RPUs
  (default 128; some Regions allow up to 1024). Set a usage limit
  (`create-usage-limit --usage-type serverless-compute`, with `--amount`, `--period` of daily, weekly or monthly,
  and `--breach-action` of `log`, `emit-metric` or `deactivate`) and consider a workgroup `maxCapacity`, so a runaway
  dashboard has a ceiling. Pick for intermittent or analyst workloads.
- Either way: enable audit logging, enhanced VPC routing for private S3 access, and automated snapshots
  (RG/RA3 retention 1 to 35 days) plus cross-Region copy.

## 2. Table design
```sql
CREATE TABLE sales (
  sale_id      BIGINT        ENCODE az64,
  customer_id  INT           ENCODE az64,
  sale_date    DATE          ENCODE az64,
  amount       DECIMAL(12,2) ENCODE az64,
  region       VARCHAR(16)   ENCODE lzo
)
DISTKEY (customer_id)
COMPOUND SORTKEY (sale_date, customer_id);
```
- AWS recommends `DISTSTYLE AUTO` and sort key `AUTO` so Redshift chooses and adjusts (automatic table
  optimization), and `ENCODE AUTO` is the default for tables. Explicit keys help when you know the join pattern.
- **Distribution**: distribute the fact table and its most-joined, largest filtered dimension on the common column
  (collocated join, a fact table has one distribution key); pick a high-cardinality column in the filtered result
  set; other joins are not collocated.
- Check skew and health in `svv_table_info`: `skew_rows` (rows in the fullest slice over the emptiest),
  `unsorted` (percent unsorted), `stats_off` (0 current, 100 out of date), `tbl_rows` (includes rows marked for
  deletion) versus `estimated_visible_rows` (does not).
- **Sort key**: lead with the timestamp column when recent data is queried most; a range-filtered or equality-filtered
  column also makes a good sort key because Redshift tracks per-block minimum and maximum values and skips blocks.
- Primary, foreign and unique keys are informational, not enforced; declare them if your ETL guarantees them, since
  the planner uses them as hints and assumes they are valid (wrong declarations can return wrong results).

## 3. Loading and unloading
```sql
COPY sales FROM 's3://bucket/sales/2026/10/' IAM_ROLE 'arn:aws:iam::<ACCOUNT_ID>:role/redshift-s3'
  FORMAT AS PARQUET;               -- or CSV GZIP IGNOREHEADER 1 DELIMITER ',' TIMEFORMAT 'auto' MAXERROR 10
UNLOAD ('SELECT * FROM sales WHERE sale_date < ''2025-01-01''')
  TO 's3://bucket/archive/sales_' IAM_ROLE '<ROLE_ARN>' FORMAT AS PARQUET PARTITION BY (sale_date) ALLOWOVERWRITE;
```
- `COPY` loads in parallel when the prefix matches multiple files or splittable files; a file that cannot be split is
  loaded serially. Redshift splits uncompressed CSV and Parquet/ORC files of 128 MB or more. For many-file loads
  Advisor suggests a multiple of the slice count with files of roughly equal size, 1 MB to 1 GB compressed. Row by
  row `INSERT ... VALUES` is the anti-pattern.
- Upsert: `COPY` into a staging table then `MERGE INTO target USING staging ON ... WHEN MATCHED THEN UPDATE SET ...
  WHEN NOT MATCHED THEN INSERT ...` (`MERGE` also supports `DELETE` and `REMOVE DUPLICATES`).
- Auto-ingest: an auto-copy job (`COPY JOB CREATE ...` with an S3 event integration), zero-ETL integrations and
  streaming ingestion into a materialized view.
- Load errors: `sys_load_error_detail` (the SYS monitoring view) lists failed loads.

## 4. Maintenance: VACUUM and ANALYZE
- Deletes and updates leave rows marked for deletion; unsorted appends weaken block skipping. Auto vacuum and auto
  analyze run in the background; for churn-heavy tables schedule `VACUUM DELETE ONLY`, `VACUUM SORT ONLY` or
  `VACUUM FULL table TO 95 PERCENT` (`FULL` is the default) in a quiet window, and run `ANALYZE table PREDICATE
  COLUMNS` after big loads.
- Health signals are the `svv_table_info` columns above.
- A deep copy (`CREATE TABLE new (LIKE old)`, `INSERT INTO new SELECT * FROM old`, swap) can beat a huge VACUUM.

## 5. Redshift Spectrum (query S3 in place)
```sql
CREATE EXTERNAL SCHEMA lake FROM DATA CATALOG DATABASE 'lake' IAM_ROLE '<ROLE_ARN>' CREATE EXTERNAL DATABASE IF NOT EXISTS;
CREATE EXTERNAL TABLE lake.events (user_id BIGINT, ts TIMESTAMP, payload VARCHAR(4000))
  PARTITIONED BY (dt DATE) STORED AS PARQUET LOCATION 's3://bucket/events/';
ALTER TABLE lake.events ADD IF NOT EXISTS PARTITION (dt='2026-10-15') LOCATION 's3://bucket/events/dt=2026-10-15/';
SELECT dt, count(*) FROM lake.events WHERE dt BETWEEN '2026-10-01' AND '2026-10-15' GROUP BY 1;
```
- Partitions must be registered (`ALTER TABLE ... ADD PARTITION` or a crawler); filter on partition columns to prune.
- Performance guidance from the docs: use Parquet (text formats scan the whole file), use multiple files larger
  than 64 MB and of similar size, select the fewest columns, and partition on common query predicates. Prices were
  not checked.
- Pattern: hot data in Redshift tables, older years `UNLOAD`ed to partitioned Parquet and queried through a view.
- Lake Formation permissions apply if the catalog is governed; the role needs Glue, S3 and Lake Formation access.

## 6. Workload management
- **Auto WLM**: `auto_wlm: true` is the default; queues have a `priority` of `highest`, `high`, `normal` (default),
  `low` or `lowest`, set per queue in the parameter group `wlm_json_configuration`. Example:
  ```json
  [{"user_group":["bi"],"priority":"high","query_group":[],"auto_wlm":true,"concurrency_scaling":"auto",
    "rules":[{"rule_name":"kill_runaway","predicate":[{"metric_name":"query_execution_time","operator":">","value":1800}],"action":"abort"}]},
   {"user_group":["etl"],"priority":"normal","auto_wlm":true},
   {"priority":"low","auto_wlm":true,"concurrency_scaling":"auto"}]
  ```
- **Query monitoring rules** per queue: `log`, `hop` (manual WLM), `abort`, `change_query_priority` on metrics such as
  `query_execution_time`, `scan_row_count`, `nested_loop_join_row_count` and `return_row_count`; see the QMR skill.
- **Concurrency scaling** (`concurrency_scaling: auto` on a queue) sends eligible queries to transient clusters
  instead of queuing. Reads and common writes (`COPY`, `INSERT`, `DELETE`, `UPDATE`, `CTAS`, `VACUUM`) are
  supported; write support needs RG or RA3 nodes. Not supported: interleaved sort key tables, temporary tables,
  system or catalog tables, Python UDFs, write operations on `DISTSTYLE ALL` or identity-column tables. The cluster
  count is capped by the `max_concurrency_scaling_clusters` parameter.
- **Short query acceleration** (SQA) runs predicted-short read-only queries in a dedicated space. In the JSON,
  `short_query_queue` defaults to false and is set per parameter group; the maximum runtime is dynamic by default.
  Advisor recommends enabling it when it sees benefit.
- Manual WLM (fixed slots and memory) still exists; Auto WLM manages concurrency and memory itself.
- Diagnose queueing and plans with `sys_query_history`, `sys_query_detail` and `EXPLAIN`.

## 7. Sharing and serving
- **Data sharing**: `CREATE DATASHARE ...; ALTER DATASHARE ... ADD SCHEMA/TABLE ...; GRANT USAGE ON DATASHARE ... TO
  NAMESPACE/ACCOUNT`. Live access without copies across clusters, workgroups, accounts and Regions, between
  provisioned and Serverless; it supports reads and writes (`SELECT`, `INSERT`, `UPDATE` grants). Use it to isolate
  BI compute from ETL compute.
- **Materialized views** (`AUTO REFRESH YES`) with automatic query rewrite speed repeated aggregations; see the
  materialized views skill.
- Result caching: `SET enable_result_cache_for_session TO off` when benchmarking.

## Gotchas
- Elastic resize does not sort tables or reclaim disk space.

## Verify
- [ ] `svv_table_info`: top-20 tables by size have acceptable `skew_rows`, `unsorted` and `stats_off`.
- [ ] `EXPLAIN` of top dashboard queries does not broadcast large tables (`DS_BCAST_INNER`).
- [ ] A large `COPY` from many similarly sized files completes with no rows in `sys_load_error_detail`.
- [ ] A Spectrum query over a partitioned prefix scans only the requested partitions.
- [ ] During an ETL run, dashboard queue time stays within SLO.

## Checked
Date: 2026-10-27. Documentation release: Amazon Redshift Database Developer Guide and Management Guide (latest),
botocore redshift-serverless 2021-04-21 model. Confirmed: Serverless base capacity range and default, usage limit
parameters, `svv_table_info` column meanings, constraint behaviour, `ENCODE AUTO` default, COPY splitting rules,
`MERGE` syntax, Spectrum performance guidance, WLM priority values, `auto_wlm` default, concurrency scaling
support and limits, SQA default, data sharing scope, `UNLOAD` and `VACUUM` options. Removed RPU 8-512 and the
60-second billing minimum, Spectrum and free-credit price claims, numeric skew and size thresholds with no source,
the `CRITICAL` priority, "SQA on by default" (the setting defaults to false), the `VARCHAR`-length, timestamp and
leader-node gotchas that no page confirmed, and the RA3-only restriction on data sharing.
Method: documentation only; no commands were run.
