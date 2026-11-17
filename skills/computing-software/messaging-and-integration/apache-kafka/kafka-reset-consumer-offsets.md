---
id: computing-software.messaging-and-integration.apache-kafka.kafka-reset-consumer-offsets
name: kafka-reset-consumer-offsets
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, reset-offsets, kafka-consumer-groups-sh, to-datetime, shift-by]
level: advanced
status: docs-checked
description: "Reset a consumer group's offsets with kafka-consumer-groups.sh --reset-offsets: dry-run, execute, export and the scenario flags."
sources:
  - https://kafka.apache.org/42/operations/basic-kafka-operations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move a group's committed offsets safely.

Preconditions: the command handles one group at a time, the consumer instances must be inactive, and you must pick a scope with `--all-topics` or `--topic` (unless using `--from-file`). See KIP-122.

Execution modes:
- default: display which offsets would be reset
- `--execute`: perform the reset
- `--export`: write the results as CSV

Scenario flags:
- `--to-datetime 'YYYY-MM-DDThh:mm:ss.sss'`
- `--to-earliest`, `--to-latest`
- `--shift-by <n>` (positive or negative)
- `--from-file` (CSV of offsets)
- `--to-current`
- `--by-duration 'PnDTnHnMnS'`
- `--to-offset <offset>`

Out-of-range targets are clamped to the available range: if the log end is 10 and you ask to shift to 15, offset 10 is selected.

Example:
`bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --reset-offsets --group my-group --topic topic1 --to-latest`
Add `--execute` to apply it. Output lists TOPIC, PARTITION and NEW-OFFSET.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Basic Kafka operations page (Managing consumer groups). Removed: closing 'typical flow' paragraph (editing exported CSV and feeding back was not on the page).

Method: documentation only; no commands were run.
