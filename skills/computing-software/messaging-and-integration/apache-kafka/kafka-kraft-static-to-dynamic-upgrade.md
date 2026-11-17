---
id: computing-software.messaging-and-integration.apache-kafka.kafka-kraft-static-to-dynamic-upgrade
name: kafka-kraft-static-to-dynamic-upgrade
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, kraft, kraft-version, kafka-features-sh]
level: advanced
status: docs-checked
description: "Upgrade a static KRaft controller quorum to a dynamic one by raising kraft.version to 1 and swapping controller.quorum.voters."
sources:
  - https://kafka.apache.org/42/operations/kraft/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move a cluster from a static to a dynamic controller quorum. Supported since Apache Kafka 4.1 (kraft.version=1, release version 4.1).

1. Check the current level:
`bin/kafka-features.sh --bootstrap-controller localhost:9093 describe`
If `FinalizedVersionLevel` for `kraft.version` is 0, it must be raised to at least 1.

2. Upgrade all feature versions:
`bin/kafka-features.sh --bootstrap-server localhost:9092 upgrade --release-version 4.1`
or only the KRaft feature:
`bin/kafka-features.sh --bootstrap-server localhost:9092 upgrade --feature kraft.version=1`

3. After confirming the upgrade succeeded, edit the config on all nodes, controllers and brokers: remove `controller.quorum.voters` and add
```
controller.quorum.bootstrap.servers=controller1.example.com:9093,controller2.example.com:9093,controller3.example.com:9093
controller.listener.names=CONTROLLER
```
alongside the existing `process.roles` and `node.id`.

The `metadata.version` feature is listed separately in the same describe output.

ZooKeeper clusters cannot go straight to KRaft on 4.x: migration requires a bridge release, and the last bridge release is Kafka 3.9, so follow the 3.9 documentation.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 KRaft operations page (Upgrade, ZooKeeper to KRaft Migration). Removed: closing 'order matters' paragraph (restated step 3 with extra claims).

Method: documentation only; no commands were run.
