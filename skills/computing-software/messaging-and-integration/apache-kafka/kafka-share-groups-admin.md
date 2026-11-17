---
id: computing-software.messaging-and-integration.apache-kafka.kafka-share-groups-admin
name: kafka-share-groups-admin
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, share-groups, kafka-share-groups-sh, delete-offsets]
level: practitioner
status: docs-checked
description: "Administer share groups with kafka-share-groups.sh: list, describe start offset and lag, reset offsets and delete."
sources:
  - https://kafka.apache.org/42/operations/basic-kafka-operations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage Kafka share groups.

List: `bin/kafka-share-groups.sh --bootstrap-server localhost:9092 --list`

Describe: `bin/kafka-share-groups.sh --bootstrap-server localhost:9092 --describe --group my-share-group` shows GROUP, TOPIC, PARTITION, START-OFFSET and LAG. START-OFFSET is the earliest offset for in-flight records still being evaluated for delivery; some records after it may already be done. The admin client needs DESCRIBE access to all topics used by the group.

Other describe options:
- `--members`: members and their assignment; two members can be assigned the same partition because they share it.
- `--offsets`: the default.
- `--state`: coordinator, state and #MEMBERS.

Reset offsets (options are `--dry-run` or `--execute`; scenarios `--to-datetime`, `--to-earliest`, `--to-latest`):
`bin/kafka-share-groups.sh --bootstrap-server localhost:9092 --reset-offsets --group my-share-group --topic topic1 --to-latest --execute`

Delete offsets for one topic:
`bin/kafka-share-groups.sh --bootstrap-server localhost:9092 --delete-offsets --group my-share-group --topic topic1`

Delete groups (only groups with no active members can be deleted):
`bin/kafka-share-groups.sh --bootstrap-server localhost:9092 --delete --group my-share-group`

Use `kafka-groups.sh --list` to see all group types together.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Basic Kafka operations page (Managing share groups). Removed: inference about lag semantics versus consumer groups.

Method: documentation only; no commands were run.
