---
id: computing-software.messaging-and-integration.apache-kafka.kafka-producer-partitioning-and-consumer-pull
name: kafka-producer-partitioning-and-consumer-pull
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, partitioner, record-key, long-poll, consumer-offset]
level: intro
status: docs-checked
description: "Understand key-based partitioning, pull-based consumers, long polling and offset-as-position, including rewind to reprocess."
sources:
  - https://kafka.apache.org/42/design/design/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand the client model that drives Kafka design decisions.

Partitioning: the client chooses the partition, either randomly or semantically. Supplying a key hashes it to a partition, so all records for one key (for example a user id) land in one partition, allowing consumers to assume locality. The partition function can be overridden.

Pull model: consumers issue fetch requests to partition leaders, specifying an offset, and receive a chunk of log from there. A pull design means a slow consumer simply falls behind and catches up, whereas push systems can overwhelm a consumer. Pull also allows aggressive batching, since a consumer takes everything available after its position (up to a configurable maximum). To avoid busy-waiting on an empty log, fetch requests can long-poll, blocking until data arrives and optionally until a given number of bytes is available.

Position: each partition is consumed by exactly one consumer per group at a time, so the position is a single integer, the offset of the next message. That state is tiny and cheap to checkpoint, making acknowledgements cheap. A consumer can deliberately rewind to an old offset and re-consume, for instance after fixing a bug.

Batch consumers, such as periodic bulk loads, can read in parallel per topic-partition and restart from the original position on failure without duplicating data.

## Checked

Method: docs-checked 2026-11-09 against kafka.apache.org/42/design/design/ (Efficiency, Producer, Consumer, Delivery Semantics, Static Membership and Using Transactions sections read in full)
