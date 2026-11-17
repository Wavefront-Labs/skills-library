---
id: computing-software.messaging-and-integration.apache-kafka.kafka-new-consumer-rebalance-protocol
name: kafka-new-consumer-rebalance-protocol
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, kip-848, group-protocol, group-consumer-assignors, group-remote-assignor]
level: advanced
status: docs-checked
description: "Enable the KIP-848 consumer rebalance protocol with group.protocol=consumer and know the server configs and limitations."
sources:
  - https://kafka.apache.org/42/operations/consumer-rebalance-protocol/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: adopt the next-generation consumer rebalance protocol (GA since Kafka 4.0). It is fully incremental and no longer relies on a global synchronization barrier, so rebalances are faster and groups scale better. Groups on the new protocol are called Consumer groups; old ones are Classic groups.

Server side: enabled automatically since 4.0, controlled by the `group.version` feature flag. The server now controls:
- `group.consumer.heartbeat.interval.ms`
- `group.consumer.session.timeout.ms`
- `group.consumer.assignors`: defaults are the uniform and range assignors; the first is the default unless the consumer picks another. Custom server assignors implement ConsumerGroupPartitionAssignor and are listed by class name.

Client side: not enabled by default. Set `group.protocol=consumer`. Optionally set `group.remote.assignor` to override the server default. `subscribe(SubscriptionPattern)` subscribes to a regular expression in RE2J format, evaluated on the server.

No longer usable with the new protocol: `heartbeat.interval.ms`, `session.timeout.ms`, `partition.assignment.strategy`, `enforceRebalance()`.

Upgrade offline: stop the group, restart members with group.protocol=consumer. Online: roll out members with that setting; the first new member converts the group, only if the classic assignor embeds no custom metadata. Downgrade is the reverse.

Limitations: client-side assignors are unsupported (KAFKA-18327); rack-aware assignment is not fully supported (KAFKA-17747).

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Consumer Rebalance Protocol page. Removed: nothing.

Method: documentation only; no commands were run.
