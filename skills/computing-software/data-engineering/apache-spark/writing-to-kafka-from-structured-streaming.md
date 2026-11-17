---
id: computing-software.data-engineering.apache-spark.writing-to-kafka-from-structured-streaming
name: writing-to-kafka-from-structured-streaming
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, structured-streaming, spark-kafka-sink, kafka-sink, at-least-once, idempotent-producer, apache-kafka]
level: practitioner
status: docs-checked
description: "Write Spark Structured Streaming output to Kafka: required key/value columns, producer options, why the sink is at-least-once, and how to dedupe downstream."
sources:
  - https://spark.apache.org/docs/latest/streaming/structured-streaming-kafka-integration.html
  - https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing to Kafka from Structured Streaming

```python
out = (events
  .select(F.col("order_id").cast("string").alias("key"),
          F.to_json(F.struct("*")).alias("value"))
  .writeStream.format("kafka")
  .option("kafka.bootstrap.servers", "b1:9092,b2:9092")
  .option("topic", "orders.enriched")          # or a per-row "topic" column
  .option("checkpointLocation", "s3a://ckpt/orders-enriched")
  .outputMode("append")
  .start())
```
- Columns: `value` (string/binary) is required; `key`, `headers` and `partition` are optional; `topic` is required unless the `topic` option is set (the option overrides a topic column).
- `kafka.bootstrap.servers` is required. The integration guide says `key.serializer`/`value.serializer` are not settable: serialise in the DataFrame instead (for example `to_json`).
- With no `key` column a null key is added; the producer calculates the partition unless a `partition` column is present, and `kafka.partitioner.class` can set a partitioner.

## Delivery guarantee: at-least-once
The integration guide says Kafka only supports at-least-once write semantics: some records may be duplicated, for example when Kafka retries a message the broker already wrote, and Structured Streaming cannot prevent that.
Handle it downstream:
- include a unique key in each record and deduplicate when reading, or in the next streaming job (`dropDuplicatesWithinWatermark`);
- or write to a transactional sink and publish from there with a connector.

## Batch writes
The integration guide covers batch queries to Kafka with the same options and the same at-least-once caveat.

## Verify
- [ ] A consumer on the topic sees the expected keys and values.
- [ ] Kill the driver mid-batch, restart, and confirm downstream dedup absorbs replayed records.

## Checked

2026-10-28. Confirmed against: Spark Kafka integration page (Writing Data to Kafka: column table, topic option override, kafka.bootstrap.servers required, key/value serializers not settable, kafka.partitioner.class, at-least-once wording), Structured Streaming guide output sinks table (Kafka sink at-least-once, foreachBatch, dropDuplicatesWithinWatermark). Removed (not confirmable in the fetched pages): producer option examples (acks, idempotence, compression, linger), headers example, to_avro, transactional-replay explanation, foreachBatch transactional producer route, console-consumer flags.

Method: documentation only; no commands were run.
