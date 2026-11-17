---
id: computing-software.cloud-infrastructure-engineering.aws.firehose-error-output-and-source-backup
name: firehose-error-output-and-source-backup
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, firehose, firehose-error-output, firehose-backup, delivery-failures, error-output-prefix, data-firehose]
level: practitioner
status: docs-checked
description: "Handle Amazon Data Firehose delivery and transformation failures: error output prefixes, source record backup, retry durations per destination, failure metrics and reprocessing."
sources: ["https://docs.aws.amazon.com/firehose/latest/dev/retry.html", "https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html", "https://docs.aws.amazon.com/firehose/latest/dev/data-transformation-failure-handling.html", "https://docs.aws.amazon.com/firehose/latest/dev/monitoring-with-cloudwatch-metrics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firehose error output and source backup

## 1. Where failed records go
- **S3 destination**: a failed delivery (missing bucket, role without access, network or S3
  errors) is retried for up to 24 hours for DirectPut sources, and up to the stream's
  retention for Kinesis Data Streams or MSK sources. Records go to the **error output prefix**
  only when Lambda processing or Parquet/ORC conversion fails.
- **Redshift**: after the retry duration (0-7200 s) the batch of S3 objects is skipped and a
  manifest file lands in the `errors/` folder for manual `COPY` backfill.
- **OpenSearch Service and Serverless**: after the retry duration (0-7200 s) the document is
  skipped and written to the `AmazonOpenSearchService_failed/` folder of the S3 backup bucket.
- **Splunk and HTTP endpoints**: after the retry duration expires the data is backed up to S3.
- **Snowflake**: retry duration 0-7200 s (default 60 s) applies only to service or network
  problems; payload, role, table or database errors are not retried and go to `snowflake-failed/`.
- If Firehose cannot deliver and also cannot write to the failure backup bucket, delivery
  effectively pauses.
- **Source record backup** (optional for S3 destinations, `S3BackupMode=Enabled`): keeps a
  copy of the raw input before transformation, so you can reprocess after fixing a bad
  Lambda.

## 2. Prefixes with expressions
```
Prefix:            data/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/
ErrorOutputPrefix: errors/!{firehose:error-output-type}/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/
```
`!{firehose:error-output-type}` becomes one of `processing-failed`,
`AmazonOpenSearchService-failed`, `splunk-failed`, `format-conversion-failed` or
`http-endpoint-failed`, and is allowed only in `ErrorOutputPrefix`. Keep errors out of the
data prefix so Athena tables over `data/` never read error files. With dynamic
partitioning, `!{partitionKeyFromQuery:customer}` and `!{partitionKeyFromLambda:...}` can
appear in `Prefix` but not in `ErrorOutputPrefix`. If `Prefix` contains expressions,
`ErrorOutputPrefix` must be set and include `!{firehose:error-output-type}`; each
evaluated prefix is limited to 512 characters.

## 3. Transformation Lambda contract
Each output record must return the same `recordId` (a mismatch counts as a transformation
failure) with `result`: `Ok`, `Dropped`, or `ProcessingFailed`, and base64 `data`.
`ProcessingFailed` records go to the `processing-failed` folder. If the invocation itself
fails (network timeout, Lambda invocation limit), Firehose retries three times by default
(`NumberOfRetries` in `ProcessorParameters`) and then skips that batch. The request and
response limit is 6 MB per synchronous invocation and the function timeout can be at most
5 minutes; keep `BufferSizeInMBs` (0.2-3 MB hint) small enough.

## 4. Metrics and alarms (namespace `AWS/Firehose`)
| Metric | Alarm |
|---|---|
| `DeliveryToS3.DataFreshness` (age of oldest record not yet delivered) | > buffer interval + margin |
| `DeliveryToS3.Success` | < 1 (fraction) |
| `DeliveryToRedshift.Success`, `DeliveryToAmazonOpenSearchService.Success`, `DeliveryToHttpEndpoint.Success` | < 1 |
| `ExecuteProcessing.Success` | < 1 |
| `FailedConversion.Records` | > 0 |
| `ThrottledRecords` (Direct PUT) | > 0 |
| `IncomingBytes` vs service limits | approaching quota |
Enable **error logging** to CloudWatch Logs in the stream configuration for detailed
failure messages per destination.

## 5. Reprocessing
- Error objects in S3 contain the raw data (base64) plus `errorCode`/`errorMessage`; fix the
  cause then replay: read files, decode, `PutRecordBatch` back into the stream (respect
  500 records / 4 MiB per call, whichever is smaller, and handle `FailedPutCount`).
- With source backup enabled, re-run from raw data after fixing the transformation.

## Verify
- [ ] Error output prefix separate from data; Athena table excludes it.
- [ ] Alarms on DataFreshness and Success metrics per destination.
- [ ] A deliberately failing transformation sends records to `errors/processing-failed/` and the replay procedure recovers them.

## Checked

2026-10-27, AWS documentation (current release as read on that date). Firehose Developer Guide pages on delivery failures, S3 prefixes, transformation (required parameters, failure handling, Lambda limits), CloudWatch metrics and quotas; botocore firehose model. Fixed: the OpenSearch error-output-type is AmazonOpenSearchService-failed (not elasticsearch-failed); the S3 error prefix is used only for Lambda or format-conversion failures, other S3 failures retry up to 24 hours (DirectPut) or the source retention; Redshift failures produce a manifest in errors/; partition-key expressions are not allowed in ErrorOutputPrefix; the missing-recordId and whole-batch claim was replaced by the documented three-retry default. Confirmed: retry duration 0-7200 s, 6 MB and 5 minute Lambda limits, PutRecordBatch 500 records or 4 MiB, metric names, S3BackupMode, FailedPutCount.
Method: documentation only; no commands were run.
