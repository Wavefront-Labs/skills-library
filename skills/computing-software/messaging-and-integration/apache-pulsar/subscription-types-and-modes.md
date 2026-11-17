---
id: computing-software.messaging-and-integration.apache-pulsar.subscription-types-and-modes
name: subscription-types-and-modes
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [subscription-types, exclusive, failover, shared, key-shared, durable, non-durable]
level: practitioner
status: docs-checked
description: "Pick a Pulsar Exclusive, Failover, Shared or Key_Shared subscription and durable vs non-durable mode; includes the key hash ranges and the batching constraint."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/concepts-messaging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: select the subscription type that gives the delivery and ordering semantics you need.

Types (chosen when a consumer connects):
- Exclusive (the default): only one consumer may attach; a second consumer on the same subscription gets an error. On a partitioned topic that single consumer receives all partitions.
- Failover: several consumers attach, but one master consumer per partition (or per non-partitioned topic) receives messages. If the master disconnects the next consumer takes over; a handover may cause duplication or reordering. For partitioned topics, consumers are sorted by priority and then consumer name, and assigned by mod(partition index, consumer index). Extra consumers beyond the partition count stay stand-by.
- Shared: messages are distributed round-robin, each to one consumer; only individual acks are allowed.
- Key_Shared: messages with the same key or ordering key always go to the same consumer. Keys are hashed (Murmur3 32-bit) and mapped by one of three algorithms: auto-split hash range (range 0 to 65,536), auto-split consistent hashing, or sticky. Adding or removing consumers remaps some keys.

Key_Shared constraint: producers must disable batching or use key-based batching (`BatcherBuilder.KEY_BASED` in Java). Default batching can pack different keys into one batch and break the key routing.

Modes: Durable (default) keeps a persistent cursor in BookKeeper, so consumption resumes after a broker restart. NonDurable loses its cursor when the broker stops; a Reader is non-durable. A durable and a non-durable subscription can share a name but are independent. A topic with no durable subscription has its messages marked deleted.

Verify: start two consumers of the chosen type, then disconnect one and confirm which consumer receives the next messages.

## Checked

Method: docs-checked 2026-11-09 against pulsar-site docs/concepts-messaging.md (Subscriptions, subscription types and modes sections read)
