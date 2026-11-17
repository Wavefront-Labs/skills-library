---
id: computing-software.data-engineering.etl-pipeline-design.cloud-cdc-services-dms-and-datastream
name: cloud-cdc-services-dms-and-datastream
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, cdc, aws-dms, datastream, full-load-and-cdc, replication-instance, bigquery, s3-target]
level: practitioner
status: docs-checked
description: "Run managed CDC with AWS DMS or Google Datastream: full load plus ongoing replication, source prerequisites, target formats, LOB and lag settings, monitoring and common failures."
sources:
  - https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html
  - https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html
  - https://cloud.google.com/datastream/docs/overview
  - https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Monitoring.html
  - https://cloud.google.com/datastream/docs/destination-bigquery
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed CDC: AWS DMS and Google Datastream

**Goal:** replicate operational databases into a lake/warehouse without running Kafka + Debezium yourself.

## AWS DMS
Task type **full load + CDC**:
1. Source prerequisites: each engine has its own logging and permission requirements (for example binlog format and retention, logical replication settings, supplemental logging); read the DMS source-endpoint page for your engine.
2. A replication instance in the VPC with network access to source and target.
3. Endpoints: source DB, target S3 / Redshift / Kinesis / MSK.
4. Table mappings (selection + transformation rules, e.g. add prefix, drop columns).

S3 target settings for lake ingestion:
```json
{"DataFormat": "parquet", "ParquetVersion": "PARQUET_2_0", "TimestampColumnName": "dms_commit_ts",
 "DatePartitionEnabled": true, "CdcMaxBatchInterval": 60}
```
`TimestampColumnName` adds the source commit timestamp, `DatePartitionEnabled` partitions by date, and `CdcMaxBatchInterval` (seconds, default 60) with `CdcMinFileSize` decides when a CDC file is written (whichever condition is met first). Batch apply is not supported for S3 targets.
Each CDC row carries an operation indicator (I/U/D) and, with `TimestampColumnName`, the source commit timestamp; apply into your table format with a MERGE ordered by commit timestamp, and add a tie-breaker if two changes can share a timestamp.

Key task settings to review: LOB handling (limited versus full LOB mode) and data validation for migrations; check the DMS task-settings reference for names and defaults.

Monitor CloudWatch: `CDCLatencySource`, `CDCLatencyTarget`, `CDCIncomingChanges`, and task status. If `CDCLatencySource` is nearly the same as `CDCLatencyTarget`, check the source side first; if target latency is much higher, look at the apply side.

## Google Datastream
- Check the Datastream overview for supported sources, destinations and connectivity options before choosing it.
- BigQuery destination with **merge** write mode keeps tables mirroring the source; Datastream appends a `datastream_metadata` STRUCT column (tables without a source primary key also get an `IS_DELETED` field). The BigQuery `max_staleness` parameter trades freshness against cost. Append-only mode keeps every change event.
- Monitor stream status and latency as described in the Datastream monitoring documentation.

## Common failures (both)
| Problem | Cause |
|---|---|
| CDC stops after hours/days | binlog/WAL retention too short, or replication slot dropped |
| Postgres WAL growth on source | stalled task keeps the slot; fix or drop the slot |
| Missing updates for some tables | tables without primary keys (check each service's primary-key requirements; Datastream's BigQuery merge mode adds an `IS_DELETED` field for tables without one) |
| LOB columns truncated | limited LOB size too small |
| Schema change breaks task | DDL handling settings; some changes require task reload |

## Choosing
Managed CDC is quicker to run; Debezium/Kafka gives more control (multiple consumers, custom transforms). See each vendor's pricing page for cost.

## Verify
- [ ] Row counts and checksums of a few tables match source after full load (DMS validation or custom reconciliation).
- [ ] Alerts on latency metrics and task/stream failure.

## Checked

2026-10-28. Confirmed in the AWS DMS S3 target page: `ParquetVersion` valid values are `PARQUET_1_0` and `PARQUET_2_0`, `TimestampColumnName`, `DatePartitionEnabled`, `CdcMaxBatchInterval` (default 60 seconds), `CdcMinFileSize`, batch apply unsupported for S3; DMS monitoring page: `CDCLatencySource`, `CDCLatencyTarget`, `CDCIncomingChanges` and how to compare them; Datastream BigQuery destination page: `datastream_metadata`, `IS_DELETED`, `max_staleness`. Fixed: `ParquetVersion` value was `parquet-2-0`. Removed: source prerequisite flags, `migration-type`, `AR_H_CHANGE_SEQ`, `EnableValidation`, LOB setting names, `describe-table-statistics`, Datastream metrics and connectivity lists, cost claims.

Method: documentation only; no commands were run.
