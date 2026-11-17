---
id: computing-software.messaging-and-integration.apache-kafka.kafka-static-membership
name: kafka-static-membership
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, static-membership, group-instance-id, fenced-instance-id-exception]
level: advanced
status: docs-checked
description: "Avoid rebalances on restarts by giving each consumer a persistent group.instance.id, and watch for FencedInstanceIdException."
sources:
  - https://kafka.apache.org/42/design/design/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop code deploys and restarts from triggering full group rebalances.

With dynamic membership, the group coordinator hands out ephemeral member ids that change on restart, so a large share of tasks can move between instances during deploys, config updates or periodic restarts. For large-state applications, shuffled tasks need a long time to recover local state and cause partial or total unavailability. Static membership lets members present persistent ids; membership stays unchanged and no rebalance is triggered.

To use it:
1. Upgrade brokers and clients to 2.3 or later, and make sure brokers use `inter.broker.protocol.version` 2.3 or later.
2. Set `group.instance.id` (ConsumerConfig.GROUP_INSTANCE_ID_CONFIG) to a unique value per consumer instance in the group.
3. In Kafka Streams, one unique `group.instance.id` per KafkaStreams instance is enough, regardless of its thread count.

Failure modes:
- If the broker is older than 2.3 and the client sets `group.instance.id`, the application detects the broker version and throws an UnsupportedException.
- If two instances share an id, broker-side fencing tells the duplicate to shut down immediately with `org.apache.kafka.common.errors.FencedInstanceIdException`.

See KIP-345 for details.

## Checked

Method: docs-checked 2026-11-09 against kafka.apache.org/42/design/design/ (Efficiency, Producer, Consumer, Delivery Semantics, Static Membership and Using Transactions sections read in full)
