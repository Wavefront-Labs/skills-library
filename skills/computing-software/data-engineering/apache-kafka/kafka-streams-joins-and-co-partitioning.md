---
id: computing-software.data-engineering.apache-kafka.kafka-streams-joins-and-co-partitioning
name: kafka-streams-joins-and-co-partitioning
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-streams, co-partitioning, stream-table-join, stream-stream-join, foreign-key-join, joinwindows, globalktable-join, topologyexception]
level: advanced
status: docs-checked
description: "Join in Kafka Streams correctly: co-partitioning requirements, stream-stream windows, stream-table temporal semantics, KTable foreign-key joins and GlobalKTable joins."
sources:
  - https://kafka.apache.org/39/streams/developer-guide/dsl-api/
  - https://cwiki.apache.org/confluence/display/KAFKA/KIP-213+Support+non-key+joining+in+KTable
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Joins and co-partitioning in Kafka Streams

**Goal:** joins that return correct results, which in Kafka Streams depends on how input topics are partitioned.

## Co-partitioning rules
For KStream-KStream, KStream-KTable and KTable-KTable (primary-key) equi-joins, input data must be co-partitioned so records with the same key reach the same stream task:
1. Both sides keyed by the **same key**.
2. Same **number of partitions**.
3. Same **partitioning strategy** on all producers (watch librdkafka vs Java defaults).
Kafka Streams only partly verifies this: at partition assignment it checks that the partition counts of both sides match. Mismatched keys or partitioners give silently missing joins. If counts differ, repartition the topic with fewer partitions (e.g. `repartition(Repartitioned.numberOfPartitions(n))`).

## Join types
| Join | Semantics |
|---|---|
| KStream-KStream | Windowed: `JoinWindows.ofTimeDifferenceWithNoGrace(Duration.ofMinutes(5))`; both sides buffered in window stores. inner / left / outer |
| KStream-KTable | Each stream record looks up the table's **current** value at processing time (not event time). inner / left. Table updates do not emit |
| KTable-KTable | Result is a KTable updated when either side changes |
| KTable-KTable FK | `orders.join(customers, Order::customerId, joiner)`: non-key join; no co-partitioning needed, Streams ensures it internally (KIP-213) |
| KStream-GlobalKTable | Key extractor picks the lookup key; no co-partitioning needed; table fully replicated |

## Stream-table timing trap
If the table record (customer created) arrives slightly after the stream record (order placed), a KStream-KTable join misses it (inner) or yields null (left). Mitigations:
- A versioned table (versioned key-value store with history retention) makes the stream-table join use the table version for the stream record's timestamp; a stream record older than the table's history retention is dropped.
- `max.task.idle.ms` controls how long a task waits for data on all of its inputs before processing, which affects whether joins produce out-of-order results.

## Example
```java
KStream<String, Payment> payments = b.stream("payments.v1");
KStream<String, Order> orders = b.stream("orders.v1");
orders.join(payments,
    (o, p) -> new Paid(o, p),
    JoinWindows.ofTimeDifferenceWithNoGrace(Duration.ofMinutes(30)))
  .to("orders.paid.v1");
```

## Checked
2026-10-28. Confirmed on the Kafka 3.9 DSL and configuration pages: co-partitioning requirements and the partial runtime check of partition counts, no co-partitioning for GlobalKTable and foreign-key joins, `JoinWindows`/`SlidingWindows` factory naming style, versioned tables in stream-table joins, `max.task.idle.ms` purpose. Removed: the `TopologyException` message, version numbers for foreign-key joins and versioned stores, `StreamJoined.as` naming, the grace-based example arguments that the page does not show for `JoinWindows`.
Method: documentation only; no commands were run.

## Verify
- [ ] `kafka-topics.sh --describe` confirms identical partition counts for joined topics.
- [ ] Topology test with the table record arriving after the stream record behaves as designed.
- [ ] Join output rate roughly equals expected match rate (no silent drop from a keying mismatch).
