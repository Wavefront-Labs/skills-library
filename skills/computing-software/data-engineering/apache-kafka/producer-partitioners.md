---
id: computing-software.data-engineering.apache-kafka.producer-partitioners
name: producer-partitioners
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-producer, sticky-partitioner, custom-partitioner, partitioner-class, murmur2, uniform-sticky, partition-key, hot-partition, librdkafka-partitioner]
level: advanced
status: docs-checked
description: "Control Kafka record placement: murmur2 key hashing, sticky partitioning for null keys, librdkafka hash mismatches, and when a custom partitioner is justified."
sources:
  - https://kafka.apache.org/39/configuration/producer-configs/
  - https://cwiki.apache.org/confluence/display/KAFKA/KIP-794%3A+Strictly+Uniform+Sticky+Partitioner
  - https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Producer partitioners

**Goal:** records with the same key always land together (ordering), load spreads evenly, and every producer language agrees on placement.

## Default behaviour (Java client)
- **Explicit partition** on the record is used as given.
- **Key present:** the partition is chosen from a hash of the key (the producer configuration page). Same key -> same partition while the partition count is unchanged. `partitioner.ignore.keys=true` makes the producer ignore keys.
- **Key null:** the built-in uniform sticky logic (KIP-794) fills a batch for one partition, then switches; with `partitioner.adaptive.partitioning.enable` (default true) it adapts to broker performance, and `partitioner.availability.timeout.ms` (default 0, disabled) marks a partition unavailable when its broker cannot take produce requests.
- `DefaultPartitioner` and `UniformStickyPartitioner` are deprecated (KIP-794): leave `partitioner.class` unset to get the built-in logic.

## Cross-language mismatch
librdkafka-based clients (confluent-kafka-python/Go/.NET) default to `partitioner=consistent_random` (CRC32 hash of the key; empty and null keys are randomly partitioned), not murmur2. A Python producer and a Java producer writing the same key go to **different partitions**, breaking ordering and co-partitioning with Kafka Streams. Fix in librdkafka clients:
```python
Producer({"bootstrap.servers": B, "partitioner": "murmur2_random"})   # "functionally equivalent to the default partitioner in the Java Producer"
```

## When a custom partitioner is justified
- Hot key isolation: route a known giant tenant to dedicated partitions.
- Geo/tenant pinning where consumers are partition-assigned manually.
Set `partitioner.class` to your implementation (it overrides the adaptive and `partitioner.ignore.keys` behaviour). Every producer to that topic must use the same partitioner, and consumers joining by key (Streams) must agree.

## Alternatives to custom code
- Composite keys (`tenant:shard`) to split a hot key, accepting per-shard ordering.
- More partitions up front so hash collisions matter less.

## Checked
2026-10-28. Confirmed against the Kafka 3.9 producer configuration page (key hash, `partitioner.adaptive.partitioning.enable`, `partitioner.availability.timeout.ms`, `partitioner.ignore.keys`), KIP-794 (uniform sticky partitioning, deprecated `DefaultPartitioner`/`UniformStickyPartitioner`) and librdkafka CONFIGURATION.md (`partitioner` values, default `consistent_random`, `murmur2_random` equivalent to the Java default). Removed: the murmur2 formula, version gate, `RoundRobinPartitioner`, custom partitioner code, kcat and the 20% figure.
Method: documentation only; no commands were run.

## Verify
- [ ] Produce the same key from each client language; a consumer shows the same partition for each.
- [ ] Per-partition byte rates are roughly even (broker metrics).
