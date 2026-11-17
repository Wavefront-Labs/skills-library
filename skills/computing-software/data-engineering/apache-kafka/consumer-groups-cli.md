---
id: computing-software.data-engineering.apache-kafka.consumer-groups-cli
name: consumer-groups-cli
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-consumer-groups-cli, consumer-groups, consumer-lag, group-state, delete-group, kafka-cli, offsets]
level: practitioner
status: docs-checked
description: "Inspect and manage Kafka consumer groups with kafka-consumer-groups.sh: list, describe members/offsets/state, read lag, delete groups and offsets, and interpret states."
sources:
  - https://kafka.apache.org/documentation/#basic_ops_consumer_group
  - https://kafka.apache.org/documentation/#basic_ops_consumer_lag
  - https://github.com/apache/kafka/blob/trunk/tools/src/main/java/org/apache/kafka/tools/consumer/group/ConsumerGroupCommandOptions.java
  - https://github.com/apache/kafka/blob/trunk/group-coordinator/src/main/java/org/apache/kafka/coordinator/group/GroupCoordinatorConfig.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kafka-consumer-groups.sh

**Goal:** answer "who is consuming what, how far behind, and is the group healthy" from the CLI, and clean up dead groups.

Put client security settings in a file and pass `--command-config client.properties` to every command on a secured cluster.

## List and describe
```bash
kafka-consumer-groups.sh --bootstrap-server $BS --list
kafka-consumer-groups.sh --bootstrap-server $BS --list --state          # with state column (--list also takes --type)
kafka-consumer-groups.sh --bootstrap-server $BS --describe --group billing
kafka-consumer-groups.sh --bootstrap-server $BS --describe --group billing --members --verbose
kafka-consumer-groups.sh --bootstrap-server $BS --describe --group billing --state
kafka-consumer-groups.sh --bootstrap-server $BS --describe --all-groups
```
Default describe (`--offsets`) columns in the docs example: `TOPIC PARTITION CURRENT-OFFSET LOG-END-OFFSET LAG CONSUMER-ID HOST CLIENT-ID`. `--members` lists active members (`--verbose` adds their partition assignment), and `--state` shows `COORDINATOR (ID)`, `ASSIGNMENT-STRATEGY`, `STATE` and `#MEMBERS`.

## Group states
| State | Meaning |
|---|---|
| `Stable` | members assigned, consuming |
| `PreparingRebalance` / `CompletingRebalance` (classic protocol), `Assigning` / `Reconciling` (consumer protocol) | rebalancing; persistent = members flapping (poll interval breaches, crash loops) |
| `Empty` | no members; committed offsets expire `offsets.retention.minutes` after the group becomes empty (default 10080 minutes, 7 days) |
| `Dead` | listed as a group state by Kafka; the group is gone or unknown to the coordinator |

## Lag interpretation
LAG = log-end - committed. A group committing only every N seconds shows sawtooth lag. Alert on lag **trend** or time-lag (lag / produce rate), not a fixed count. For Kafka Streams apps, also check repartition topics.

## Delete
```bash
kafka-consumer-groups.sh --bootstrap-server $BS --delete --group old-app          # deletes offsets and ownership info; --group can repeat
kafka-consumer-groups.sh --bootstrap-server $BS --delete-offsets --group billing --topic retired_topic
```
`--delete-offsets` deletes a group's offsets for the named topics (one group at a time, several topics), which stops it reporting lag on a topic it no longer reads.

## Reset (pointer)
`--reset-offsets` works on one group at a time with a scope (`--all-topics` or `--topic`, unless `--from-file`) and a scenario: `--to-datetime` (`YYYY-MM-DDThh:mm:ss.sss`), `--by-duration` (`PnDTnHnMnS`), `--to-earliest`, `--to-latest`, `--to-current`, `--shift-by`, `--to-offset`, `--from-file`. Execution modes are `--dry-run` (the default), `--execute` and `--export` (CSV); consumers must be inactive first. See the reset-offsets skill for replay procedures.

## Gotchas
- `--all-groups` applies a command to every consumer group; on a large cluster prefer scripting per group.
- Lag only reflects offsets committed to Kafka: a consumer that keeps offsets in an external store will not show meaningful lag here.

## Verify
- [ ] Every production group shows `Stable` with all partitions owned.
- [ ] Retired groups deleted; no orphan lag alerts.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed (ConsumerGroupCommandOptions source and operations docs): `--list`/`--state`/`--type`, `--describe` with `--members`, `--verbose`, `--offsets`, `--state`, `--all-groups`, `--delete`, `--delete-offsets`, the reset-offsets scenarios and execution modes, group state names (GroupState enum), and the `offsets.retention.minutes` default of 7 days counted from the group becoming empty (GroupCoordinatorConfig). Removed: the unconfirmed `CONSUMER-ID`/`CURRENT-OFFSET` dash interpretations, the Spark and Flink commit remarks, the `assign()` remark, the "must be Empty" delete rule and the sawtooth-lag claim.

Method: documentation only; no commands were run.
