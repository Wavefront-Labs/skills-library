---
id: computing-software.messaging-and-integration.apache-kafka.kafka-transactional-exactly-once
name: kafka-transactional-exactly-once
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, transactions, transactional-id, read-committed, enable-auto-commit]
level: advanced
status: docs-checked
description: "Build a consume-process-produce loop with transactional.id, isolation.level=read_committed and enable.auto.commit=false, and handle abort exceptions."
sources:
  - https://kafka.apache.org/42/design/design/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get exactly-once processing with the plain producer and consumer, the way Kafka Streams does it. Only the producer is transactional; it also commits the consumer's offsets inside the transaction.

Required config:
- Consumer: `isolation.level=read_committed` and `enable.auto.commit=false`.
- Producer: `transactional.id=<unique name>`. Only the producer has this setting; a restarted application aborts any in-flight transaction from the previous instance.

Design rules:
- Partition assignment ensures one consumer in the group processes each partition.
- The producer writes records and the consumer offsets atomically.
- Use one producer instance per consumer instance to cope with rebalancing.

Commit or abort writes transaction marker records; that is how read_committed consumers skip aborted data. After an abort, the application must reset the consumer position itself to reprocess.

Exception categories (the standardized hierarchy): RetriableException and RefreshRetriableException are handled inside the client; AbortableException requires aborting the transaction and resetting the consumer position; ApplicationRecoverableException requires your own recovery including restarting the producer; InvalidConfigurationException does not require a producer restart; KafkaException is general.

Simple policy: discard and recreate the producer and consumer. The group rebalances and fetches the last committed offset, rewinding to before the aborted transaction.

## Checked

Method: docs-checked 2026-11-09 against kafka.apache.org/42/design/design/ (Efficiency, Producer, Consumer, Delivery Semantics, Static Membership and Using Transactions sections read in full)
