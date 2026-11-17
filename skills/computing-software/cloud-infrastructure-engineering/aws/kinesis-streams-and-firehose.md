---
id: computing-software.cloud-infrastructure-engineering.aws.kinesis-streams-and-firehose
name: kinesis-streams-and-firehose
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, kinesis, kinesis-data-streams, firehose, data-firehose, streaming, shards, on-demand-mode, provisioned-mode, enhanced-fan-out, kcl, kpl, partition-key, iterator-age, provisionedthroughputexceeded, lambda-event-source-mapping, dynamic-partitioning, s3-delivery, hot-shard]
level: practitioner
status: docs-checked
description: "Run Kinesis Data Streams and Data Firehose: shard sizing vs on-demand, partition keys, hot shards, KCL and Lambda consumers, enhanced fan-out, iterator age, Firehose S3 delivery."
sources: ["https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html", "https://docs.aws.amazon.com/streams/latest/dev/enhanced-consumers.html", "https://docs.aws.amazon.com/firehose/latest/dev/dynamic-partitioning-enable.html", "https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html", "https://docs.aws.amazon.com/firehose/latest/dev/limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kinesis Data Streams and Data Firehose — streaming ingest that does not fall behind

**Goal:** a stream that absorbs producer bursts, delivers to every consumer with bounded lag,
and lands records in S3/OpenSearch/Redshift without hand-written sinks.

## 1. Pick Streams vs Firehose
| Need | Use |
|---|---|
| Multiple consumers, replay within retention (24 h–365 d), sub-second latency, custom processing | **Kinesis Data Streams** |
| "Just land it in S3/Redshift/OpenSearch/Splunk/HTTP" with buffering, optional Lambda transform, no consumer code | **Data Firehose** (buffering hints of 1-128 MiB and 0-900 s; near-real-time, not real-time) |
| Both | Streams as source → Firehose as a consumer (Firehose can read a stream directly) |

## 2. Capacity: shards or on-demand
- A shard = **1 MB/s or 1,000 records/s in**, **2 MB/s out** shared by all standard consumers,
  5 `GetRecords`/s. Size provisioned streams at `ceil(max(in_MBps, in_records/1000))` with ~30 % headroom.
- **On-demand** mode scales automatically (up to double the peak write throughput seen in the
  previous 30 days); use it for spiky or unknown load, switch to provisioned once the profile
  is flat (you can switch modes twice per 24 h per stream).
- Resharding provisioned streams: `aws kinesis update-shard-count --target-shard-count N
  --scaling-type UNIFORM_SCALING`. Child shards keep ordering per partition key; consumers
  must handle shard end and start children (KCL does this).

## 3. Partition keys and hot shards
- Records hash by partition key to a shard. Low-cardinality keys (`tenant=big-customer`)
  make a hot shard and `ProvisionedThroughputExceededException` while other shards idle.
- Use high-cardinality keys (device id, request id) unless you need per-key ordering;
  if you need ordering per customer *and* one customer is huge, shard by `customer#bucket`.
- Watch `WriteProvisionedThroughputExceeded` and per-shard metrics (enable **enhanced
  shard-level metrics**) to find the hot one.

## 4. Producers
- Batch with `PutRecords` (up to 500 records / 10 MiB per call); check the response — it is
  **partial-failure**: `FailedRecordCount > 0` means retry only the failed entries.
- **KPL** aggregates many user records into one Kinesis record (consumers need KCL or a
  deaggregation library).
- Retry with exponential backoff + jitter.

## 5. Consumers
- **Lambda event source mapping**: set `BatchSize`, `MaximumBatchingWindowInSeconds`,
  `ParallelizationFactor` (1-10, default 1: concurrent batches per shard),
  `BisectBatchOnFunctionError`, `MaximumRetryAttempts`, and an on-failure destination.
  Return `batchItemFailures` (`ReportBatchItemFailures`) so one poison record
  does not block the shard forever.
- **KCL** (a Java library; other languages use the MultiLangDaemon): load balancing across
  workers, checkpointing and shard-count changes handled for you. Use the latest version;
  KCL 2.6.0 or earlier should be upgraded to 2.6.1 or later (a rare condition can block shard
  processing when stream capacity changes).
- **Enhanced fan-out** (`register-stream-consumer`): each consumer gets a dedicated 2 MB/s per
  shard pushed over HTTP/2 (about 70 ms typical latency) instead of sharing 2 MB/s with polling
  consumers. Up to 20 registered consumers per stream (50 with On-demand Advantage). Use it
  when you have several consumers or latency matters.

## 6. The alarm that matters: iterator age
`GetRecords.IteratorAgeMilliseconds` (stream) / `IteratorAge` (Lambda) = how far behind the
newest consumer is. Alarm at a fraction of retention (e.g. 1 h on 24 h retention) — if it reaches
retention you are **losing data silently**. Fix by adding shards, raising
`ParallelizationFactor`, or speeding the function.

## 7. Firehose delivery
- Buffer hints: `SizeInMBs` (1-128) and `IntervalInSeconds` (0-900); whichever is reached
  first flushes. Small buffers = many small S3 objects = Athena pain.
- **Dynamic partitioning** (S3 destination only) builds S3 prefixes from record fields
  (`!{partitionKeyFromQuery:customer_id}`) → Hive-style `customer_id=.../dt=.../` prefixes
  for Athena/Glue partitions. It can only be enabled when you create the stream, and cannot be
  disabled afterwards.
- Convert JSON → Parquet/ORC in-flight (needs a schema in the AWS Glue Data Catalog).
- Transform with a Lambda (6 MB payload limit for request and response, 5 minute function
  timeout; return `recordId`, `result` `Ok|Dropped|ProcessingFailed`, base64 `data`). Failed
  records go to the S3 error prefix.
- `DirectPut` streams have a combined `PutRecord`/`PutRecordBatch` quota per stream: 5 MiB/s,
  2,000 requests/s and 500,000 records/s in US East (N. Virginia), US West (Oregon) and Europe
  (Ireland); 1 MiB/s, 1,000 requests/s and 100,000 records/s elsewhere. Firehose raises the limit
  automatically when throttled, so keep retrying, and request an increase for sudden bursts.

## Gotchas
- Firehose delivers at least once; retries can create duplicates for every destination except
  S3, Apache Iceberg tables and Snowflake, so make other sinks idempotent.
- `GetRecords` throttling (`ReadProvisionedThroughputExceeded`) with several standard consumers
  → move to enhanced fan-out rather than adding shards.
- A new on-demand stream starts at 4 MB/s write and 8 MB/s read; the maximum on-demand ceiling
  differs by Region (10 GB/s write in US East (N. Virginia), US West (Oregon), Europe (Ireland);
  200 MB/s elsewhere unless raised). Check the quotas page for your Region.

## Verify
- [ ] Load test at 1.5× expected peak shows zero `WriteProvisionedThroughputExceeded`.
- [ ] Shard-level metrics show even distribution (no shard above ~70 % of its limit).
- [ ] Iterator-age alarm exists and pages below retention.
- [ ] Poison record test: one bad record is sent to the on-failure destination; shard keeps moving.
- [ ] Firehose objects land in partitioned prefixes as Parquet and are queryable in Athena.

## Checked

2026-10-27, AWS documentation (current release as read on that date). Kinesis quotas, capacity-mode, enhanced fan-out and KCL pages; Firehose quotas, dynamic partitioning, format conversion, transformation and delivery pages; Lambda Kinesis page; botocore kinesis, firehose and lambda models. Fixed: PutRecords limit is 10 MiB per call (not 5 MiB); dynamic partitioning can be enabled only at creation and never disabled (not "cannot be toggled later"); buffer interval range is 0-900 for all destinations in the API model. Confirmed: shard rates, on-demand double-the-30-day-peak behaviour and two mode switches per 24 h, enhanced fan-out 2 MB/s, 70 ms and 20/50 consumers, ParallelizationFactor 1-10, Firehose DirectPut quotas, Glue schema for Parquet/ORC, at-least-once duplicates, 6 MB and 5 minute Lambda limits. Removed unsourced claims: Lambda producers and KPL, the KCL DynamoDB lease detail, SQS/SNS destination list, billing and per-second polling remarks.
Method: documentation only; no commands were run.
