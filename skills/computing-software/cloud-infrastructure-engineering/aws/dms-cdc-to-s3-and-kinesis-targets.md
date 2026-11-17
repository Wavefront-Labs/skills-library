---
id: computing-software.cloud-infrastructure-engineering.aws.dms-cdc-to-s3-and-kinesis-targets
name: dms-cdc-to-s3-and-kinesis-targets
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dms, dms-s3-target, dms-kinesis-target, cdc, data-lake-ingestion]
level: advanced
status: docs-checked
description: "Stream database changes with DMS into S3 (Parquet, CDC op column, partitioning) or Kinesis/MSK (JSON records with metadata) for data lakes and event pipelines."
sources: ["https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Kinesis.html", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Kafka.html", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Monitoring.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CDC to S3 and Kinesis targets

## 1. S3 target
```bash
aws dms create-endpoint --endpoint-identifier lake-s3 --endpoint-type target --engine-name s3 \
  --s3-settings '{"ServiceAccessRoleArn":"arn:aws:iam::<ACCOUNT_ID>:role/dms-s3","BucketName":"raw-lake-<ACCOUNT_ID>",
    "BucketFolder":"cdc/orders","DataFormat":"parquet","ParquetVersion":"parquet-2-0",
    "IncludeOpForFullLoad":true,"TimestampColumnName":"dms_ts",
    "DatePartitionEnabled":true,"DatePartitionSequence":"YYYYMMDDHH","DatePartitionDelimiter":"SLASH",
    "CdcMaxBatchInterval":60,"CdcMinFileSize":32000,"EncryptionMode":"sse-kms","ServerSideEncryptionKmsKeyId":"<KEY_ARN>"}'
```
- `EncryptionMode` values: the API model lists `sse-s3` and `sse-kms`; the DMS guide writes `SSE_S3` and `SSE_KMS`. Check which spelling your CLI version accepts.
- Full load files are named `LOAD00000001.<ext>`, `LOAD00000002.<ext>` and so on under
  `schema/table/`. In CDC output the first column of each row is the operation, `I`, `U` or `D`; with
  `IncludeOpForFullLoad` full-load rows get an `I` too. The timestamp column is the one named by `TimestampColumnName`.
- Downstream: apply changes in order of the timestamp column, for example with Glue/Spark or Athena `MERGE INTO` an Iceberg table.
- `CdcMaxBatchInterval` (default 60 seconds) and `CdcMinFileSize` (default 32,000 KB) trade latency
  for fewer small files; a file is written when either condition is met.

## 2. Kinesis target
```bash
aws dms create-endpoint --endpoint-identifier events-kds --endpoint-type target --engine-name kinesis \
  --kinesis-settings 'StreamArn=arn:aws:kinesis:<REGION>:<ACCOUNT_ID>:stream/orders-cdc,MessageFormat=json-unformatted,
    ServiceAccessRoleArn=arn:aws:iam::<ACCOUNT_ID>:role/dms-kinesis,IncludeTransactionDetails=true,
    IncludePartitionValue=true,PartitionIncludeSchemaTable=true,IncludeTableAlterOperations=true'
```
- Each record has a `data` part (the row) and a `metadata` part (operation, timestamp, schema, table
  name, transaction details when `IncludeTransactionDetails` is on and the source supports it: Oracle,
  SQL Server, PostgreSQL, MySQL).
- Choose the partition key per table with an object-mapping rule `partition-key-type`: `schema-table`,
  `transaction-id`, `primary-key`, `constant` or `attribute-name`. Kinesis has no deduplication, so
  consumers must handle duplicates. Do not enable `BatchApplyEnabled` for a Kinesis target (task failure and data loss).
- MSK/Kafka: `--engine-name kafka --kafka-settings Broker=<host:port>,Topic=orders-cdc,...`. Supported
  `SecurityProtocol` values are `plaintext`, `ssl-encryption`, `ssl-authentication` and `sasl-ssl` (SASL
  mechanisms `scram-sha-512` or `plain`); the MSK security group must allow the replication instance.
  Pick the broker port that matches that protocol; IAM access control is not among the listed options.

## 3. Task settings
Use `full-load-and-cdc` or `cdc` with a start position. For Kinesis (and Kafka) CDC throughput the
task settings `ParallelApplyThreads` (default 0, maximum 32 for Kinesis), `ParallelApplyBufferSize`
(default 100, maximum 1,000) and `ParallelApplyQueuesPerThread` (default 1, maximum 512) apply; monitor
`CDCLatencyTarget` in CloudWatch.

## Verify
- [ ] An update on the source appears as an `U` record in S3 or Kinesis within the batch interval.

## Checked

2026-10-27, AWS documentation (current release as read on that date). AWS DMS User Guide S3, Kinesis and Kafka target pages and monitoring page; botocore dms 2016-01-01 model (S3Settings, KinesisSettings, KafkaSettings and enums). Fixed: the unsourced primary-key default partition key was replaced by the documented partition-key-type values; BatchApply must not be enabled for Kinesis targets; the Kafka example port 9098 implied IAM access control, which is not a supported DMS Kafka SecurityProtocol (plaintext, ssl-encryption, ssl-authentication, sasl-ssl with scram-sha-512 or plain); added the ParallelApply task setting defaults and maxima; EncryptionMode spelling conflict noted (API model sse-kms, guide SSE_KMS). Confirmed: all S3Settings and KinesisSettings keys used, ParquetVersion, DatePartition values, CdcMaxBatchInterval default 60 s, CdcMinFileSize default 32000 KB, I/U/D first column, LOAD file naming, CDCLatencyTarget metric. Removed the Op-column claim for full-load without IncludeOpForFullLoad.
Method: documentation only; no commands were run.
