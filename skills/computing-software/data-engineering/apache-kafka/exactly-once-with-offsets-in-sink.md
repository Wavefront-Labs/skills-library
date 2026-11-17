---
id: computing-software.data-engineering.apache-kafka.exactly-once-with-offsets-in-sink
name: exactly-once-with-offsets-in-sink
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, exactly-once, offsets-in-sink, kafka-consumer, external-offsets, seek, rebalance-listener, postgres-sink]
level: advanced
status: docs-checked
description: "Get exactly-once from Kafka into a database by committing results and consumer offsets in the same DB transaction, then seeking from stored offsets on assignment."
sources:
  - https://kafka.apache.org/documentation/#semantics
  - https://kafka.apache.org/37/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html
  - https://kafka.apache.org/37/javadoc/org/apache/kafka/clients/consumer/ConsumerRebalanceListener.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exactly-once by storing offsets in the sink

**Goal:** Kafka transactions only cover Kafka-to-Kafka. For Kafka -> Postgres/MySQL/warehouse, make the write and the offset atomic in the *sink*.

## Pattern
1. Table in the sink: `kafka_offsets(group_id, topic, partition, next_offset, primary key(group_id, topic, partition))`.
2. Consumer with `enable.auto.commit=false`.
3. On partition assignment, read `next_offset` from the table and `seek()`.
4. For each batch: in one DB transaction, write results **and** upsert the new `next_offset` per partition; commit.
5. Optionally also `commitAsync()` to Kafka purely for lag monitoring (never read back).

## Java sketch
```java
consumer.subscribe(List.of("payments"), new ConsumerRebalanceListener() {
  public void onPartitionsAssigned(Collection<TopicPartition> parts) {
    for (TopicPartition tp : parts) {
      Long off = repo.loadOffset(GROUP, tp);           // null -> not stored yet
      if (off != null) consumer.seek(tp, off); else consumer.seekToBeginning(List.of(tp));
    }
  }
  public void onPartitionsRevoked(Collection<TopicPartition> parts) { /* batch already committed */ }
});
while (running) {
  ConsumerRecords<String, Payment> recs = consumer.poll(Duration.ofMillis(500));
  if (recs.isEmpty()) continue;
  try (Connection c = ds.getConnection()) {
    c.setAutoCommit(false);
    writeRows(c, recs);
    for (TopicPartition tp : recs.partitions()) {
      long next = recs.records(tp).get(recs.records(tp).size() - 1).offset() + 1;
      upsertOffset(c, GROUP, tp, next);
    }
    c.commit();
  }
}
```
```sql
insert into kafka_offsets(group_id, topic, partition, next_offset) values (?,?,?,?)
on conflict (group_id, topic, partition) do update set next_offset = excluded.next_offset;
```

## Why it works
A crash before DB commit: neither rows nor offsets persist; restart re-reads the same records. After commit: both persist; restart seeks past them. No duplicates, no gaps.

## Variants
- Idempotent upsert keyed by `(topic, partition, offset)` or a business key: simpler, at-least-once delivery with effectively-once results. Choose this if the sink cannot hold offsets transactionally.

## Gotchas
- With `assign()` instead of `subscribe()` there is no listener; seek once at startup.
- Partition count changes: new partitions have no stored offset; decide earliest vs latest explicitly.
- Long DB transactions with large batches hold locks; cap `max.poll.records` and keep batch commit time well under `max.poll.interval.ms`.
- Multiple consumer groups writing the same table need `group_id` in the offsets key.

## Verify
- [ ] Kill -9 the consumer mid-batch repeatedly in a test; row count equals source record count, no duplicates.
- [ ] `kafka_offsets.next_offset` equals log-end offset when caught up.

## Checked
2026-11-01. Confirmed in the Kafka 3.9 design doc (message delivery semantics: store the consumer offset in the same place as the output), KafkaConsumer javadoc (`seek`, `seekToBeginning`, `ConsumerRebalanceListener.onPartitionsRevoked/onPartitionsAssigned`) and ConsumerConfig javadoc (`max.poll.records`, `max.poll.interval.ms`). Removed unconfirmed claims about Spark, Flink and the Connect JDBC sink.
Method: documentation only; no commands were run.
