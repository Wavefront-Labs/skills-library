---
id: computing-software.data-engineering.apache-flink.kafka-source-per-partition-watermarks
name: kafka-source-per-partition-watermarks
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, per-partition-watermarks, kafka-source, flink-kafka-connector, idleness, event-time]
level: advanced
status: docs-checked
description: "Get correct event-time progress from Flink's KafkaSource: watermarks per Kafka partition, idle partitions, partition discovery, and why post-source assignment is worse."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/#watermark-strategies-and-the-kafka-connector
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/kafka/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Per-partition watermarks in the Kafka source

A Flink source subtask often reads several Kafka partitions. Each partition is ordered-ish by time, but interleaving them makes the combined stream heavily out of order. If watermarks are generated after the source, the bound must cover the skew between partitions; if generated per partition, it only needs to cover disorder within a partition.

```java
KafkaSource<Event> src = KafkaSource.<Event>builder()
    .setBootstrapServers(bs).setTopics("events").setGroupId("agg")
    .setProperty("partition.discovery.interval.ms", "60000")
    .setDeserializer(KafkaRecordDeserializationSchema.valueOnly(new EventSchema()))
    .build();
WatermarkStrategy<Event> ws = WatermarkStrategy
    .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(5))
    .withTimestampAssigner((e, kafkaTs) -> e.eventTime())     // or use kafkaTs (record timestamp)
    .withIdleness(Duration.ofMinutes(2));
DataStream<Event> s = env.fromSource(src, ws, "events");
```
Passing the strategy to `fromSource` makes the reader run one generator **per split (partition)** and emit the minimum across its splits. This is the default and the right way with FLIP-27 sources. (Calling `assignTimestampsAndWatermarks` on the DataStream after the source does not.)

## Idle partitions
A partition with no traffic stops its watermark and holds back the subtask's minimum forever: windows never close. `withIdleness(d)` marks a split idle after `d` without records so it is excluded. Choose `d` larger than normal gaps in traffic; a partition that is merely slow but marked idle produces late data when it resumes.

## More subtasks than partitions
The Kafka source does not go idle automatically when parallelism is higher than the number of partitions (per the Flink Kafka connector page): lower the parallelism or add an idle timeout to the watermark strategy.

## Skewed partitions
One partition far behind (consumer lag concentrated in it) keeps the watermark low while others race ahead, buffering lots of window state. Watermark alignment (`withWatermarkAlignment("group", Duration.ofSeconds(20), Duration.ofSeconds(1))`) pauses fast splits; alignment needs a source that supports it (see the watermark docs on alignment).

## Kafka record timestamp
`kafkaTs` in the assigner is the Kafka record timestamp (CreateTime or LogAppendTime); use it only if producers set it to event time.

## Verify
- [ ] Watermark in Flink UI tracks max event time minus ~bound, not minus inter-partition skew.
- [ ] Stopping traffic to one partition does not stall windows beyond the idleness timeout.

## Checked

2026-10-28. Confirmed: withIdleness, withWatermarkAlignment and the idle-source discussion on the watermark page; partition.discovery.interval.ms on the Kafka connector page. Removed: a WRONG claim that KafkaSource marks partition-less subtasks idle, plus a version gate and legacy-consumer notes.

Method: documentation only; no commands were run.
