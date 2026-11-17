---
id: computing-software.messaging-and-integration.apache-kafka.kafka-rack-awareness
name: kafka-rack-awareness
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, broker-rack, rack-awareness, replica-placement]
level: practitioner
status: docs-checked
description: "Spread partition replicas across racks or availability zones by setting broker.rack on each broker."
sources:
  - https://kafka.apache.org/42/operations/basic-kafka-operations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: extend broker-failure guarantees to rack or availability-zone failure.

Set the rack on each broker:
`broker.rack=my-rack-id`

When a topic is created or modified, or replicas are redistributed, Kafka honours the rack constraint so replicas span as many racks as possible; a partition spans min(#racks, replication-factor) different racks. The same mechanism works for other groupings such as EC2 availability zones.

The replica assignment algorithm keeps the number of leaders per broker constant regardless of how brokers are spread over racks, which keeps throughput balanced.

Failure mode: if racks hold different numbers of brokers, replica assignment is uneven. Racks with fewer brokers get more replicas, so they use more storage and more replication resources. Configure an equal number of brokers per rack.

## Checked

Method: docs-checked 2026-11-09 against the kafka.apache.org 4.2 basic Kafka operations page (Balancing replicas across racks). An unsupported closing paragraph on existing clusters was removed.
