---
id: computing-software.messaging-and-integration.apache-kafka.kafka-transaction-protocol-v2
name: kafka-transaction-protocol-v2
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, transaction-version, kip-890, add-partitions-to-txn-retry-backoff-ms]
level: advanced
status: docs-checked
description: "Enable the stronger server-side transaction protocol with transaction.version=2 and tune add.partitions.to.txn retry backoff."
sources:
  - https://kafka.apache.org/42/operations/transaction-protocol/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn on Transactions Server Side Defense (KIP-890), available from Kafka 4.0.

With it, the producer epoch is bumped on every transaction, so each transaction contains exactly the intended messages and duplicates are not written into the next transaction. It requires 4.0 or newer producer clients.

Enabling: the protocol is on by default since 4.0 and governed by the `transaction.version` feature flag. Set it with the storage tool when creating a new cluster, or dynamically on an existing cluster with the features tool: `transaction.version=2`. Producers do not need a restart; they upgrade at the next connect or reconnect, and never mid-transaction, only at the start of the next transaction after learning of the server upgrade. Downgrade works the same way and is safe.

Performance: one server-side add-partitions call replaces the client add plus server verify. The old hardcoded 20ms client backoff on CONCURRENT_TRANSACTIONS (KAFKA-5477) can no longer be used; instead the server retries adding the partition a few times itself before returning the error. This can raise reported produce latency, while end-to-end transaction latency (begin to commit) stays about the same. Tune with `add.partitions.to.txn.retry.backoff.ms` and `add.partitions.to.txn.retry.backoff.max.ms`.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 transaction-protocol page. Replaced the unconfirmed endTransaction-asynchrony explanation with the page's KAFKA-5477 backoff note; latency claim softened to "about the same". No hands-on run.
