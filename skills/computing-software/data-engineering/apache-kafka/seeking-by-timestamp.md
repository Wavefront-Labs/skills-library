---
id: computing-software.data-engineering.apache-kafka.seeking-by-timestamp
name: seeking-by-timestamp
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-consumer, offsetsfortimes, seek, replay, time-based-replay]
level: practitioner
status: docs-checked
description: "Start a Kafka consumer at a point in time in code with offsetsForTimes and seek, handling partitions with no newer records and timestamp-quality caveats."
sources:
  - https://kafka.apache.org/39/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html#offsetsForTimes(java.util.Map)
  - https://kafka.apache.org/documentation/#topicconfigs_message.timestamp.type
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Seeking by timestamp (offsetsForTimes)

**Use when:** the app itself must replay from a time (incident recovery from 09:00, a backfill job), rather than resetting a group's offsets from the CLI.

```java
long from = Instant.parse("2026-10-17T09:00:00Z").toEpochMilli();
consumer.subscribe(List.of("orders"), new ConsumerRebalanceListener() {
  public void onPartitionsRevoked(Collection<TopicPartition> p) {}
  public void onPartitionsAssigned(Collection<TopicPartition> parts) {
    Map<TopicPartition, Long> query = parts.stream().collect(Collectors.toMap(tp -> tp, tp -> from));
    Map<TopicPartition, OffsetAndTimestamp> found = consumer.offsetsForTimes(query);
    for (TopicPartition tp : parts) {
      OffsetAndTimestamp o = found.get(tp);
      if (o != null) consumer.seek(tp, o.offset());
      else consumer.seekToEnd(List.of(tp));     // no record at/after `from` in this partition
    }
  }
});
```
With `assign()`, call `offsetsForTimes` and `seek` right after assigning.


## Semantics
- Returns the **earliest offset whose timestamp >= the target**, per partition, using the broker time index.
- `null`/-1 for a partition means no such record (all records are older): seek to end, not beginning.
- The call blocks, and the consumer does not have to be assigned the partitions. A negative timestamp throws `IllegalArgumentException`; `TimeoutException` after `default.api.timeout.ms`; `UnsupportedVersionException` if the broker cannot look up by timestamp.
- Accuracy depends on how timestamps were set (`message.timestamp.type`: `CreateTime` is producer-supplied, `LogAppendTime` is broker-assigned), so producer clock skew affects what "time" means.
- To stop at a time as well, read until `record.timestamp() > to` per partition and then pause that partition.

## Do not forget offsets
If the consumer commits to a group, the seek is persisted on the next commit. For one-off replays use a fresh `group.id` (or no commits) so the production group is untouched.

## Verify
- [ ] First record processed per partition has timestamp >= target, and the previous offset's timestamp < target.

## Checked
2026-11-01. Confirmed against the Kafka 3.9 `KafkaConsumer` javadoc (`offsetsForTimes`: earliest offset with timestamp >= target, null when none, blocking, exceptions) and the topic config reference (`message.timestamp.type`). Removed: Python offset -1 claim, retention/log-start behaviour, index-scanning detail.
Method: documentation only; no commands were run.
