---
id: computing-software.messaging-and-integration.apache-pulsar.partitioned-topics-and-routing
name: partitioned-topics-and-routing
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [partitioned-topics, routing-modes, hashing-scheme, ordering-guarantee, murmur3]
level: practitioner
status: docs-checked
description: "Use Pulsar partitioned topics for throughput: routing modes, per-key and per-producer ordering, and why to switch the hashing scheme to Murmur3_32Hash."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/concepts-messaging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: raise topic throughput beyond one broker while keeping the ordering your application needs.

A normal topic is served by a single broker, which caps its throughput. A partitioned topic is implemented as N internal topics (N = partition count) spread across brokers automatically. Partitioned topics must be created explicitly through the admin API, where the partition count is given. Partitioning only affects what happens between publish and consume: subscription types behave the same as on normal topics. Decide routing from throughput needs and subscription type from application semantics.

Routing modes (`MessageRoutingMode`) are set on the producer:
- `RoundRobinPartition` (the default): with no key, publishes across all partitions round-robin for maximum throughput; with a key, hashes it to a partition. Round-robin switches at the batching delay boundary rather than per message so that batching stays effective.
- `SinglePartition`: with no key, picks one partition at random and sends everything there; with a key, hashes the key to choose the partition.
- `CustomPartition`: a custom `MessageRouter` implementation (Java client) decides.

Ordering guarantees:
- Per-key-partition: same key goes to the same partition in order; use SinglePartition or RoundRobinPartition and give each message a key.
- Per-producer: all messages from one producer in order; use SinglePartition with no key.

Hashing scheme (`HashingScheme` on the producer builder): `JavaStringHash` is the default; `Murmur3_32Hash` is the alternative. Gotcha: JavaStringHash is not suitable when producers come from several client languages, so use `Murmur3_32Hash` there to get the same partition for the same key.

## Checked

2026-11-03. Confirmed against the Pulsar messaging concepts page, partitioned topics and routing sections: routing modes (RoundRobinPartition is the default), round-robin at the batching-delay boundary, `CustomPartition` with `MessageRouter`, per-key-partition and per-producer ordering, `HashingScheme` with JavaStringHash default and the Murmur3_32Hash recommendation for multi-language producers. Added: RoundRobinPartition is the default. Removed: the generic Verify line.

Method: documentation only; no commands were run.
