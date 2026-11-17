---
id: computing-software.data-engineering.apache-flink.filesystem-sink-and-rolling-policies
name: filesystem-sink-and-rolling-policies
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-connectors, filesink, rolling-policy, bulk-formats, parquet-writer, bucket-assigner, pending-files, exactly-once, compaction, s3-sink]
level: advanced
status: docs-checked
description: "Write Flink streams to S3/HDFS with FileSink: row vs bulk formats, rolling on checkpoint, bucket assigners for date paths, in-progress/pending files, compaction and small files."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/filesystem/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/table/filesystem/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FileSink and rolling policies

**Goal:** land a stream into object storage as well-sized, exactly-once files that downstream batch engines can read.

## Row vs bulk formats
```java
// Row-encoded (text/JSON lines): flexible rolling
FileSink<String> rows = FileSink
    .forRowFormat(new Path("s3://<BUCKET>/raw/events/"), new SimpleStringEncoder<String>("UTF-8"))
    .withRollingPolicy(DefaultRollingPolicy.builder()
        .withRolloverInterval(Duration.ofMinutes(15))
        .withInactivityInterval(Duration.ofMinutes(5))
        .withMaxPartSize(MemorySize.ofMebiBytes(256)).build())
    .withBucketAssigner(new DateTimeBucketAssigner<>("'dt='yyyy-MM-dd'/hr='HH", ZoneId.of("UTC")))
    .build();

// Bulk-encoded (Parquet/ORC/Avro): rolls ONLY on checkpoint
FileSink<Event> parquet = FileSink
    .forBulkFormat(new Path("s3://<BUCKET>/silver/events/"), parquetWriterFactory /* a BulkWriter.Factory from the Flink Parquet format page */)
    .withBucketAssigner(new DateTimeBucketAssigner<>("'dt='yyyy-MM-dd", ZoneId.of("UTC")))
    .withOutputFileConfig(OutputFileConfig.builder().withPartPrefix("events").withPartSuffix(".parquet").build())
    .build();
stream.sinkTo(parquet);
```

## Exactly-once mechanics
Part files go through **in-progress -> pending -> finished**. Pending files are committed (renamed/finalised) only when the checkpoint that covers them completes. Therefore:
- **Checkpointing must be enabled**, or files never finalise (they stay `.inprogress`/pending forever).
- Checkpoint interval = file latency and file size driver for bulk formats: 1-minute checkpoints x parallelism 32 = 32 small Parquet files per minute.
- Downstream readers must ignore `.` / `_` prefixed in-progress files (most engines do).

## Small files
- Lower sink parallelism (`sinkTo(...).setParallelism(4)`) or key by bucket before the sink.
- Longer checkpoint interval for bulk formats (trade off recovery time).
- Enable compaction: `FileSink...enableCompact(FileCompactStrategy.Builder.newBuilder().setNumCompactThreads(4).enableCompactionOnCheckpoint(5).build(), compactor)`, or in SQL `'auto-compaction' = 'true'`, `'compaction.file-size' = '256MB'`.
- Or write to a table format (Iceberg/Paimon/Delta sinks) whose maintenance handles compaction and gives atomic commits plus a catalog.

## Table API equivalent
```sql
CREATE TABLE events_sink (..., dt STRING) PARTITIONED BY (dt) WITH (
  'connector' = 'filesystem', 'path' = 's3://<BUCKET>/silver/events/', 'format' = 'parquet',
  'sink.rolling-policy.file-size' = '256MB', 'sink.rolling-policy.rollover-interval' = '15 min',
  'sink.partition-commit.trigger' = 'partition-time', 'sink.partition-commit.delay' = '1 h',
  'sink.partition-commit.policy.kind' = 'success-file,metastore', 'auto-compaction' = 'true');
```
Partition commit writes `_SUCCESS` (and/or registers the partition in a Hive metastore) once the watermark passes partition end + delay.

## S3 specifics
Use the `flink-s3-fs-hadoop` plugin under `plugins/`: the Flink S3 page says it is the only stable implementation that provides a RecoverableWriter for the FileSink (`flink-s3-fs-presto` does not).

## Verify
- [ ] Finished files appear after each checkpoint; no files stuck in-progress after a clean stop-with-savepoint.
- [ ] Average file size within target; `_SUCCESS` markers per partition when using partition commit.
- [ ] Kill and restore from checkpoint: no duplicate rows in the landed data.

## Checked

2026-10-28. Confirmed: enableCompact and enableCompactionOnCheckpoint on the FileSink page; auto-compaction and compaction.file-size on the table filesystem page; S3 plugin support on the Flink S3 page. Removed: a wrong recommendation of the presto S3 plugin for FileSink, a version gate, an unconfirmed multipart note and an unconfirmed Parquet writer factory name.

Method: documentation only; no commands were run.
