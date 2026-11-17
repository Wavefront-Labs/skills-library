---
id: computing-software.data-engineering.databricks.streaming-from-kafka-event-hubs-and-kinesis
name: streaming-from-kafka-event-hubs-and-kinesis
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-kafka-ingestion, kinesis, event-hubs, structured-streaming]
level: advanced
status: docs-checked
description: "Ingest Kafka and Kinesis streams on Databricks into Delta: reader options, row schemas, lag metrics, AvailableNow, Kinesis EFO and data-loss handling."
sources:
  - https://docs.databricks.com/aws/en/connect/streaming/kafka
  - https://docs.databricks.com/aws/en/connect/streaming/kinesis
  - https://learn.microsoft.com/en-us/azure/databricks/connect/streaming/kafka
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming from Kafka, Event Hubs and Kinesis on Databricks

**Goal:** a reliable bronze ingestion stream from a message bus into a Delta table.

## Kafka
```python
from pyspark.sql.functions import from_json, col

df = (spark.readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "<bootstrap-server>:9092")
  .option("subscribe", "<topic-name>")
  .option("databricks.serviceCredential", "<service-credential-name>")
  .load())

(df.select(from_json(col("value").cast("string"), "event_type STRING, event_ts TIMESTAMP").alias("value"))
  .select("value.*")
  .writeStream.format("delta")
  .option("checkpointLocation", "<checkpoint-path>")
  .trigger(availableNow=True)
  .toTable("catalog.schema.events_table"))
```
- `kafka.bootstrap.servers` is required for batch and streaming reads. Choose topics with exactly one of `subscribe` (comma-separated list), `subscribePattern` (Java regex) or `assign` (JSON of topic partitions).
- Batch reads use `spark.read` with `startingOffsets` and `endingOffsets`. For incremental batch loading Databricks recommends `Trigger.AvailableNow`.
- Authentication options on Databricks include Unity Catalog service credentials (`databricks.serviceCredential`), SASL/SSL, and cloud-specific options for AWS MSK, Azure Event Hubs and Google Cloud Managed Kafka; see the Authentication section of the Kafka page.
- SQL: `read_kafka` (Databricks Runtime 13.3 LTS and above); streaming use needs Lakeflow pipelines or streaming tables in Databricks SQL.
- Rows come back as `key` (binary), `value` (binary), `topic` (string), `partition` (int), `offset` (long), `timestamp` (timestamp), `timestampType` (int). Key and value are always byte arrays: use `cast("string")`, `from_json`, `from_avro` or `from_protobuf` to decode.
- Kafka kafka-clients in Databricks Runtime 13.3 LTS and above enables idempotent writes by default. Writing to a Kafka sink on version 2.8.0 or below with ACLs but no IDEMPOTENT_WRITE fails with `Cannot execute transactional method because we are in an error state`; upgrade Kafka or set `kafka.enable.idempotence` to `false` on the writer.
- Writer: `topic` overrides any `topic` column; the DataFrame needs a `value` column (STRING or BINARY), optional `key`, `headers`, `topic`, `partition`.

## Event Hubs
Event Hubs is listed on the Kafka page as a cloud-specific authentication option. Look up its exact connection settings in the Authentication section of the Kafka page before use.

## Kinesis
```python
df = (spark.readStream.format("kinesis")
  .option("streamName", "<stream-name>")
  .option("region", "<aws-region>")
  .load())
```
- Specify either `streamName` or `streamARN` (the latter on Databricks Runtime 16.1 and above), never both. Do not switch between them for an active query; start a new query with a fresh checkpoint instead.
- Authentication: Unity Catalog connection, service credential, or alternatives such as an instance profile or access keys.
- Schema: `partitionKey`, `data` (binary), `stream`, `shardId`, `sequenceNumber`, `approximateArrivalTimestamp`. Cast `data` to string to read it.
- `Trigger.AvailableNow` works with Kinesis on Databricks Runtime 13.3 LTS and above; it is best-effort, and omitted records are picked up by the next batch. If fetches keep failing, raise `maxFetchDuration`.
- Enhanced fan-out (EFO): dedicated 2 MB/s per shard per consumer, maximum 20 consumers per stream, push mode. A registered EFO consumer incurs extra Kinesis charges; set `requireConsumerDeregistration` to `true` to deregister on teardown (not guaranteed after driver crashes). Override the default `databricks_`-prefixed consumer name with `consumerNamePrefix` or `consumerName`.
- Polling readers: each shard supports five GetRecords calls per second; with N polling queries on one stream set `minFetchPeriod` to at least 200ms * N.
- Removing a stream from `streamName` fails on restart with `KINESIS_SOURCE_STREAMS_REMOVED_ON_RESTART` unless `failOnDataLoss` is `false` (Databricks Runtime 19 and above).
- Writes through the ForeachSink are at least once, not exactly once.

## Practice
- Land raw bytes plus metadata in bronze; parse in silver.
- One checkpoint per stream; never share.
- On serverless compute the `availableNow` trigger is recommended for incremental streaming; use Lakeflow pipelines continuous mode for low latency.

## Gotchas
- Kinesis: if shard records expire before the query reads them, or a stream is deleted and recreated with the same name, the query fails with `KINESIS_COULD_NOT_READ_SHARD_UNTIL_END_OFFSET`. Setting `failOnDataLoss` to `false` skips the unreadable records; use it only as a temporary mitigation and fix the cause (for example a too-short retention period).

## Verify
- Kafka lag: `avgOffsetsBehindLatest`, `maxOffsetsBehindLatest`, `minOffsetsBehindLatest` and `estimatedTotalBytesBehindLatest` appear in `query.lastProgress["sources"][0]["metrics"]`. On Databricks Runtime 17.1 and above small persistent non-zero values on busy topics are expected.
- Kinesis lag: `avgMsBehindLatest`, `maxMsBehindLatest`, `minMsBehindLatest`; `maxMsBehindLatest` near zero means caught up.

## Checked
2026-11-09: read the Databricks (AWS) Kafka and Kinesis pages and the Azure Databricks Kafka page in full. Confirmed reader options, row schemas, idempotent-write note, lag metrics, AvailableNow, EFO limits, rate-limit guidance and data-loss errors. Removed unconfirmed claims: maxOffsetsPerTrigger values, SCRAM/JAAS `kafkashaded.` prefix, Event Hubs connection string settings, Kinesis `roleArn`/`initialPosition`, schema registry Avro options, Kafka `failOnDataLoss`.
Method: documentation only; no commands were run.
