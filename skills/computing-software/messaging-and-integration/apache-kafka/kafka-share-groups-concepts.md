---
id: computing-software.messaging-and-integration.apache-kafka.kafka-share-groups-concepts
name: kafka-share-groups-concepts
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, share-groups, share-consumer, share-record-lock-duration-ms]
level: practitioner
status: docs-checked
description: "Understand share groups: cooperative record consumption, acquisition locks, share.record.lock.duration.ms and the lock limit."
sources:
  - https://kafka.apache.org/42/design/design/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know when a share group fits better than a consumer group and how record delivery works.

Differences from consumer groups:
- Consumers cooperatively consume records; a partition may be assigned to several consumers.
- A share group can have more consumers than a topic has partitions.
- Records are acknowledged individually (the system is still optimized for batches).
- Delivery attempts are counted, enabling automated handling of unprocessable records.

Each share group consumes a topic independently of other share groups.

When a share consumer fetches, records are acquired with a time-limited acquisition lock, making them unavailable to other consumers in that group. The default lock duration is 30 seconds, set by the group config `share.record.lock.duration.ms`. For an acquired record the consumer can: acknowledge it, release it for another attempt, reject it (unprocessable, no more deliveries), renew it (extend the attempt), or do nothing, in which case the lock expires and the record is redelivered.

The broker limits acquired records per topic-partition per share group with the broker property `group.share.partition.max.record.locks`. Once reached, fetches temporarily yield no more records until the number of acquired records decreases (as locks naturally time out). Limiting lock duration and releasing locks automatically keeps delivery progressing even when consumers fail.

## Checked

Method: docs-checked 2026-11-09 against the kafka.apache.org 4.2 design page (The Share Consumer section). An unsupported line about kafka-share-groups.sh was removed.
