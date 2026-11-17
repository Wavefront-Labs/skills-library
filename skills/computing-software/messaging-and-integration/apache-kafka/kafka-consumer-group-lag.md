---
id: computing-software.messaging-and-integration.apache-kafka.kafka-consumer-group-lag
name: kafka-consumer-group-lag
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, kafka-consumer-groups-sh, consumer-lag, describe-group]
level: practitioner
status: docs-checked
description: "List, describe and delete consumer groups with kafka-consumer-groups.sh to read lag, members and state."
sources:
  - https://kafka.apache.org/42/operations/basic-kafka-operations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: check consumer positions and lag.

List groups: `bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list`

Describe offsets and lag:
`bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group my-group`
Columns: TOPIC, PARTITION, CURRENT-OFFSET, LOG-END-OFFSET, LAG, CONSUMER-ID, HOST, CLIENT-ID.

Extra describe options:
- `--members` lists active members with #PARTITIONS.
- `--members --verbose` also shows each member's assignment.
- `--offsets` is the default, same as plain `--describe`.
- `--state` shows coordinator, assignment strategy, state and #MEMBERS.

Permissions: if the group uses the `consumer` protocol, the admin client needs DESCRIBE access to all topics the members subscribe to; the `classic` protocol does not require DESCRIBE on all topics.

Delete groups manually:
`bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --delete --group my-group --group my-other-group`
Deletion works only if the group has no active members. Groups are also removed automatically when the last committed offset for the group expires.

To list groups of every type (consumer, share, streams) use `bin/kafka-groups.sh --bootstrap-server localhost:9092 --list`, which shows GROUP, TYPE and PROTOCOL.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Basic Kafka operations page (Managing consumer groups). Removed: nothing.

Method: documentation only; no commands were run.
