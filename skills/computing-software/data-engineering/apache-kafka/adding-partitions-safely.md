---
id: computing-software.data-engineering.apache-kafka.adding-partitions-safely
name: adding-partitions-safely
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, add-partitions, kafka-topics, key-ordering, repartition, partition-count, consumer-scaling]
level: practitioner
status: docs-checked
description: "Increase a Kafka topic's partition count without breaking keyed ordering or stateful consumers: impact analysis, the alter command, and migrate-to-new-topic alternative."
sources:
  - https://kafka.apache.org/documentation/#basic_ops_modify_topic
  - https://github.com/apache/kafka/blob/trunk/docs/operations/basic-kafka-operations.md
  - https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/clients/producer/ProducerConfig.java
  - https://github.com/apache/kafka/blob/trunk/docs/streams/developer-guide/dsl-api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adding partitions safely

**Goal:** get more consumer parallelism or throughput from a topic, knowing exactly what breaks when keys move partitions. Partitions can only be added, never removed.

## What changes
The default partitioner picks a partition from a hash of the key (the docs write `hash(key) % number_of_partitions`), so changing the partition count changes the mapping for existing keys, and Kafka does not redistribute existing data. After the change:
- New records for key K may go to a different partition than older records for K: per-key ordering is broken across the boundary.
- If K can now land in a different partition, old and new records for K can sit in different partitions, which matters for compacted topics and any consumer that rebuilds state from the topic.
- Kafka Streams joins require co-partitioned inputs: the same number of partitions on both topics and the same partitioning strategy for all writers.

Unkeyed records are sticky-partitioned (a partition is used until at least `batch.size` bytes are produced to it), so key mapping does not apply.

## Command
```bash
kafka-topics.sh --bootstrap-server $BS --describe --topic orders
kafka-topics.sh --bootstrap-server $BS --alter --topic orders --partitions 24
```
Producers pick up new partitions after the next metadata refresh (`metadata.max.age.ms`, default 5 minutes). Consumers with `auto.offset.reset=latest` can miss records produced to a new partition before they discover it; the Kafka docs recommend `auto.offset.reset=by_duration:<duration>` for consumers of topics whose partition count may grow.

## Safe procedure for keyed topics
1. Decide whether ordering across the boundary matters.
2. Pause producers (or drain), wait until consumer lag is 0.
3. Alter partitions; refresh or restart producers; resume.
4. For Kafka Streams apps, internal topics follow the application, so use the application reset tool (`kafka-streams-application-reset.sh`, preview with `--dry-run`) and rebuild state rather than mixing partition counts.

## Alternative: new topic
For compacted or strictly ordered topics, create `orders.v2` with the target count, dual-write or mirror with a re-keying job, migrate consumers, retire the old topic. Slower, but no key split.

## Sizing note
Partitions can only be added. Plan the count at creation time rather than repeatedly expanding, because each expansion changes key placement.

## Verify
- [ ] `--describe` shows new partitions with leaders and full ISR.
- [ ] All consumer groups have members assigned to new partitions (`kafka-consumer-groups.sh --describe --members --verbose`) and lag is draining.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed against the "Modifying topics" docs and the `--partitions` option text in TopicCommand: key-distribution change and the warning about keyed topics, the `auto.offset.reset=latest` loss window and the `by_duration:<duration>` recommendation, the default partitioner choosing by key hash and the sticky behaviour for unkeyed records (ProducerConfig `partitioner.class` doc), `metadata.max.age.ms` default of 5 minutes, Streams co-partitioning requirements (DSL docs), and the application reset tool. Removed: the `murmur2` and "most keys" specifics, the compaction-behaviour claim, Flink keyed state, the idempotent-upsert advice, the claim that only `earliest` is safe, and the per-partition overhead list.

Method: documentation only; no commands were run.
