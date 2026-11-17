---
id: computing-software.data-engineering.apache-kafka.exactly-once-source-connectors
name: exactly-once-source-connectors
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-connect, exactly-once-source, transactions, source-connectors, kip-618, debezium]
level: advanced
status: docs-checked
description: "Enable exactly-once delivery for Kafka Connect source connectors (KIP-618): worker and connector settings, transaction boundaries, ACLs, and which connectors support it."
sources:
  - https://kafka.apache.org/documentation/#connect_exactlyoncesource
  - https://github.com/apache/kafka/blob/trunk/docs/kafka-connect/user-guide.md
  - https://github.com/apache/kafka/blob/trunk/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/SourceConnectorConfig.java
  - https://github.com/apache/kafka/blob/trunk/connect/api/src/main/java/org/apache/kafka/connect/source/SourceTask.java
  - https://kafka.apache.org/documentation/#georeplication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exactly-once source connectors (KIP-618)

Without it, a source connector writes records, then commits offsets periodically; a crash between the two produces duplicates on restart. KIP-618 (source connectors, as of Kafka 3.3.0) writes records **and** source offsets in one Kafka transaction. Support depends on the connector: setting the worker properties is not enough if the connector cannot use the framework's capabilities.

## Enable
1. Workers (distributed mode only), rolling restart in two phases:
```properties
exactly.once.source.support=preparing   # phase 1 on all workers
exactly.once.source.support=enabled     # phase 2 after all workers are on preparing
```
2. Connector config:
```json
{
  "exactly.once.support": "required",
  "transaction.boundary": "poll",
  "offsets.storage.topic": "connect-offsets-orders-cdc"
}
```
- `exactly.once.support` is `requested` (default) or `required`. `required` forces a preflight check that the connector can provide exactly-once with this configuration, and create or validate requests fail if the worker does not have source exactly-once support enabled. Use `requested` for a connector that can do exactly-once but does not signal it; read its documentation first.
- `transaction.boundary`: `poll` (default: a transaction for every batch of records a task hands to Connect), `interval` (commit after `transaction.boundary.interval.ms`), or `connector` (the connector defines boundaries; instantiation fails if it cannot).
- `offsets.storage.topic` in the connector config gives that connector its own offsets topic.

## Requirements
- Exactly-once for source connectors works only in distributed mode; standalone workers cannot provide it.
- On a secured cluster the worker principal needs extra ACLs: `IdempotentWrite` on the Cluster resource, and Write and Describe on the transactional ids `connect-cluster-<group.id>` (used by the worker itself) and `<group.id>-<connector>-<task>` (used by each task), plus read and write on the offsets topics.
- The connector must declare support for exactly-once. MirrorMaker 2 supports it on dedicated MirrorMaker clusters as of 3.5.0 (set `exactly.once.source.support` per target cluster).
- Consumers must use `isolation.level=read_committed` to skip aborted records; the consumer default is `read_uncommitted`.

## Trade-offs
- Each transaction adds work per boundary: `poll` commits per batch, `interval` commits less often.
- Sink side is separate: for sink connectors that support it, set `consumer.isolation.level=read_committed` on the worker or allow `consumer.override.isolation.level` through the override policy.

## Verify
- [ ] `GET /connectors/<name>/status` shows RUNNING for the connector and all tasks.
- [ ] Kill a worker during heavy load; a `read_committed` consumer sees no duplicates (compare source row count to topic record count).

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: worker property `exactly.once.source.support` values and the two-phase `preparing` then `enabled` upgrade, distributed-mode-only restriction, source support as of 3.3.0, connector properties `exactly.once.support` (requested default, required semantics), `transaction.boundary` (poll default, interval, connector), `transaction.boundary.interval.ms` and `offsets.storage.topic` (SourceConnectorConfig and SourceTask source), the transactional id formats (Worker and DistributedConfig source), the IdempotentWrite ACL operation, consumer `isolation.level` default, and MirrorMaker 2 exactly-once as of 3.5.0. Removed: the broker 3.0 requirement, Debezium and Confluent connector claims, the REST-based fencing explanation and the batching-size tuning advice.

Method: documentation only; no commands were run.
