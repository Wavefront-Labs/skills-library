---
id: computing-software.data-engineering.apache-kafka.manual-partition-assignment
name: manual-partition-assignment
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-consumer, manual-partition-assignment, assign-vs-subscribe, seek, standalone-consumer]
level: advanced
status: docs-checked
description: "Use consumer.assign() instead of subscribe() when you need fixed partitions: no group rebalancing, manual offset handling, and the pitfalls with committed offsets."
sources:
  - https://kafka.apache.org/documentation/#consumerapi
  - https://kafka.apache.org/39/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manual partition assignment (assign vs subscribe)

| | `subscribe(topics)` | `assign(partitions)` |
|---|---|---|
| Who picks partitions | group coordinator, rebalances on join/leave | you (dynamic assignment and group coordination are disabled) |
| Failover | automatic | none: you restart or reassign |
| New partitions picked up | yes (metadata refresh) | no, unless you re-call assign |

## When assign() is right
- A process that must own specific partitions (one per partition in a StatefulSet; partition = shard of local state).
- Tools: reading one partition for debugging, replaying a range, offset exporters.

```java
TopicPartition tp = new TopicPartition("orders", partitionId);
consumer.assign(List.of(tp));
OffsetAndMetadata c = consumer.committed(Set.of(tp)).get(tp);
if (c != null) consumer.seek(tp, c.offset()); else consumer.seekToBeginning(List.of(tp));
while (running) {
  var records = consumer.poll(Duration.ofMillis(500));
  process(records);
  consumer.commitSync();                       // or store offsets alongside results
}
```

## Pitfalls
- **Never mix** assign and subscribe in one consumer (IllegalStateException).
- Do not share a `group.id` with a subscribe()-based group if you commit offsets: the two would overwrite each other's committed offsets. Give manual consumers their own `group.id`.
- No liveness: if the process dies, nobody consumes its partitions. You need external supervision (Kubernetes restart, your own leader election).
- Partition count changes: re-list partitions (`partitionsFor`) periodically and assign new ones.

## Verify
- [ ] Restarting the process resumes from the committed offset.

## Checked
2026-11-01. Confirmed against the Kafka 3.9 `KafkaConsumer` javadoc: manual assignment via `assign(Collection)` disables dynamic assignment and group coordination; `IllegalStateException` when mixing subscribe and assign; `committed`, `seek`, `seekToBeginning`, `partitionsFor`. Removed: group.id requirement row, framework internals, `max.poll.interval.ms` note, group-describe check. The shared-group.id warning is advice following from the committed-offset model, not a quoted doc statement.
Method: documentation only; no commands were run.
