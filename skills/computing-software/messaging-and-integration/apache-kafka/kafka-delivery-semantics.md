---
id: computing-software.messaging-and-integration.apache-kafka.kafka-delivery-semantics
name: kafka-delivery-semantics
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, delivery-semantics, at-least-once, exactly-once, idempotent-producer]
level: practitioner
status: docs-checked
description: "Choose at-most-once, at-least-once or exactly-once behaviour by ordering offset commits, processing and producer retries."
sources:
  - https://kafka.apache.org/42/design/design/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the delivery guarantee that fits the workload.

Kafka treats a message as committed once all replicas in the in-sync set (ISR) have applied it. A producer that hits a network error cannot tell whether the message was committed. Since 0.11.0.0 the producer supports idempotent delivery: the broker assigns each producer an ID and deduplicates by the sequence number sent with each message, so retries do not create duplicates. Transactions let a producer write atomically to multiple partitions.

Consumer side, depending on the order of work:
- Read, save position, then process: at-most-once (a crash can skip unprocessed messages).
- Read, process, then save position: at-least-once (a crash can reprocess messages). If messages have a primary key, updates can be made idempotent.
- Exactly-once between Kafka topics: write output and the consumer offset in one transaction; consumers use `isolation.level=read_committed`.

Defaults and options: Kafka guarantees at-least-once by default. At-most-once is achieved by disabling producer retries and committing offsets before processing a batch. For external systems, store the offset in the same place as the output (as Kafka Connect connectors do for HDFS) rather than using a two-phase commit.

In the default `read_uncommitted` isolation level, consumers see messages from aborted transactions.

## Checked

Method: docs-checked 2026-11-09 against kafka.apache.org/42/design/design/ (Efficiency, Producer, Consumer, Delivery Semantics, Static Membership and Using Transactions sections read in full)
