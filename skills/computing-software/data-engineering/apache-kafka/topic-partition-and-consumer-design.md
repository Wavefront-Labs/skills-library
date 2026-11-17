---
id: computing-software.data-engineering.apache-kafka.topic-partition-and-consumer-design
name: topic-partition-and-consumer-design
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, topics, partitions, partition-count-sizing, partition-key, message-ordering, replication-factor, min-insync-replicas, acks-all, idempotent-producer, consumer-groups, rebalancing, cooperative-sticky, offset-commit, max-poll-interval-ms, retention-ms, log-compaction, consumer-lag, confluent, msk, redpanda, event-streaming]
level: advanced
status: docs-checked
description: "Design Kafka topics and consumers: partition count and keys for ordering, RF 3 with min.insync.replicas 2 and acks=all, idempotent producers, rebalancing, offset commits, lag."
sources:
  - https://kafka.apache.org/40/configuration/producer-configs/
  - https://kafka.apache.org/40/configuration/consumer-configs/
  - https://kafka.apache.org/39/operations/basic-kafka-operations/
  - https://kafka.apache.org/40/getting-started/upgrade/
  - https://www.confluent.io/blog/how-choose-number-topics-partitions-kafka-cluster/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Kafka topic, partition and consumer design — durable, ordered, scalable

**Goal:** create a topic whose partitioning, durability and retention match the workload, and consumers that keep up without losing or reprocessing more than intended.

## 1. Choose the key first — it decides ordering
Kafka guarantees order **only within a partition**. Records with the same key go to the same partition (the producer hashes the key; the Java producer's hash is murmur2, which librdkafka can reproduce with its `murmur2` partitioner).
- Key by the entity whose events must stay ordered: `order_id`, `account_id`, `device_id`.
- Null key → records are spread across partitions, no ordering.
- **Gotcha:** a hot key (one giant tenant) pins load to one partition and one consumer. Watch per-partition byte rates; if one key dominates, sub-key it (`tenant_id:shard`) and accept per-shard ordering.
- **Gotcha:** adding partitions later does not repartition existing data, and with keyed data the key-to-partition mapping changes, which can disturb consumers that rely on it (basic operations page). Size up front.

## 2. Partition count
- Partitions cap consumer parallelism: a group can have at most one active consumer per partition.
- Estimate: `max(target_MBps / per_partition_producer_MBps, target_MBps / per_partition_consumer_MBps)`, then add headroom for growth. Measure per-partition throughput on your hardware.
- More partitions mean more open file handles, more memory in the producer and longer unavailability after an unclean broker failure (Confluent's partition-count article); do not over-provision.

## 3. Durability settings
```bash
kafka-topics.sh --bootstrap-server <BROKER>:9092 --create --topic orders.v1 \
  --partitions 12 --replication-factor 3 \
  --config min.insync.replicas=2 --config retention.ms=604800000
```
Producer:
```properties
acks=all
enable.idempotence=true          # default true since Kafka 3.0 clients
max.in.flight.requests.per.connection=5   # <=5 keeps ordering with idempotence
retries=2147483647
delivery.timeout.ms=120000
```
- RF 3 + `min.insync.replicas=2` + `acks=all` survives one broker loss without losing acknowledged writes and keeps accepting writes. With `min.insync.replicas=3`, losing one broker blocks producers.
- Keep `unclean.leader.election.enable=false` (default) — `true` trades data loss for availability.
- Idempotence dedupes producer retries per partition. For atomic writes across partitions or topics use transactions (`transactional.id`) with consumers on `isolation.level=read_committed`.

## 4. Consumers and rebalancing
- Each `group.id` gets every message once across its members. Separate apps = separate groups.
- Set `partition.assignment.strategy=org.apache.kafka.clients.consumer.CooperativeStickyAssignor` (or the newer KIP-848 consumer protocol, `group.protocol=consumer`, in Kafka 4.x / late 3.x — check your broker and client) to avoid stop-the-world rebalances.
- `group.instance.id` (static membership) prevents rebalances on quick restarts during rolling deploys.
- `max.poll.interval.ms` (default 300000 = 5 min): if processing one `poll()` batch takes longer, the consumer is kicked out and its partitions are reassigned — the classic "rebalance storm". Lower `max.poll.records` (default 500) or move slow work off the poll thread.
- `session.timeout.ms` default is 45 s in Kafka 3.0+ clients (10 s earlier).

## 5. Offset commits
- Default `enable.auto.commit=true` commits on a timer — it can commit before processing finishes (loss on crash) or after (duplicates).
- For at-least-once: `enable.auto.commit=false`, process, then `commitSync()` (or async with a final sync on shutdown). Make downstream writes idempotent so duplicates are harmless.
- `auto.offset.reset` (`latest` by default) applies only when the group has no committed offset — a new group silently skips history unless you set `earliest`.

## 6. Retention and compaction
- `cleanup.policy=delete` with `retention.ms` (default 7 days) and/or `retention.bytes` for event streams.
- `cleanup.policy=compact` keeps the latest value per key — for changelogs/state topics; a null value (tombstone) deletes the key after `delete.retention.ms`.
- Compaction requires keys and is not instant; don't rely on it for dedupe timing.

## 7. Monitor lag
`kafka-consumer-groups.sh --bootstrap-server <BROKER>:9092 --describe --group <GROUP>` shows `LAG` per partition. Alert on lag growing over time (or time-lag), not on a fixed count. One lagging partition = hot key or a stuck consumer.

Related: computing-software.data-engineering.streaming-architecture.delivery-guarantees-and-ordering.

## Verify
- [ ] `kafka-topics.sh --describe` shows RF 3, `min.insync.replicas=2`, and all partitions with full ISR.
- [ ] Producer config shows `acks=all` and `enable.idempotence=true`.
- [ ] Killing one broker during a load test causes no producer errors and no lost acknowledged messages.
- [ ] Rolling restart of consumers completes without lag spikes beyond your SLA.
- [ ] Per-partition lag is roughly even; no single partition carries most of the traffic.

## Checked
2026-10-28. Confirmed in the Kafka 3.9/4.0 producer, consumer, topic and broker config pages, the 4.0 upgrade notes and the basic operations page: `enable.idempotence` default true since 3.0, `max.in.flight.requests.per.connection` <= 5 with idempotence, `max.poll.interval.ms` 300000, `max.poll.records` 500, `session.timeout.ms` 45000, `enable.auto.commit` true, `auto.offset.reset` semantics, `CooperativeStickyAssignor`, `group.protocol` (`consumer` vs `classic`; KIP-848 GA in 4.0), `group.instance.id`, `retention.ms` 7 days, `delete.retention.ms`, `unclean.leader.election.enable`, adding partitions does not move data, `min.insync.replicas` with `acks=all` (NotEnoughReplicas). Removed: the murmur2 default-partitioner claim as Kafka behaviour, sticky-partitioner remark, the 10 MB/s and typical partition counts, and the idempotence-per-session claim.
Method: documentation only; no commands were run.
