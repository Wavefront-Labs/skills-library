---
id: computing-software.data-engineering.apache-kafka.deleting-topics-safely
name: deleting-topics-safely
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, delete-topic, kafka-topics-cli, topic-cleanup, delete-topic-enable, kafka-topic-design]
level: practitioner
status: docs-checked
description: "Delete Kafka topics without surprises: delete.topic.enable, auto-create recreating them, checking for live producers/consumers, consumer group and schema cleanup."
sources:
  - https://kafka.apache.org/documentation/#basic_ops_add_topic
  - https://github.com/apache/kafka/blob/trunk/server-common/src/main/java/org/apache/kafka/server/config/ServerConfigs.java
  - https://github.com/apache/kafka/blob/trunk/tools/src/main/java/org/apache/kafka/tools/TopicCommand.java
  - https://github.com/apache/kafka/blob/trunk/docs/streams/developer-guide/app-reset-tool.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deleting topics safely

## Before deleting
1. Confirm nobody uses it:
```bash
kafka-consumer-groups.sh --bootstrap-server $BS --describe --all-groups   # look for the topic in the output
kafka-log-dirs.sh --bootstrap-server $BS --describe --topic-list orders.v1   # size, to know what you lose
```
   Producers do not show up in any CLI; check broker metrics `kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec,topic=orders.v1` for a few days, or ACL/audit logs.
2. If a producer is still writing and `auto.create.topics.enable=true` (broker default true; most production clusters set false), the topic is **recreated immediately** with default partitions/config. Disable auto-create or stop producers first.
3. Kafka Streams internal topics (named `<application.id>-<operatorName>-<suffix>`) belong to an app: use `kafka-streams-application-reset.sh` (it requires `--application-id` and supports `--dry-run`) or delete them with the app stopped.

## Delete
```bash
kafka-topics.sh --bootstrap-server $BS --delete --topic orders.v1
kafka-topics.sh --bootstrap-server $BS --delete --topic 'tmp\..*'   # --topic also accepts a regular expression (not with --create); quote it, check with --list first
```
- Requires `delete.topic.enable=true` (default true) and the Delete operation allowed on the topic when an authorizer is enabled.
- Deletion is asynchronous: log directories are marked for deletion and removed after the delay set by `file.delete.delay.ms` (broker default `log.segment.delete.delay.ms`, 60000 ms).

## After
- Delete committed offsets of groups that only read this topic: `kafka-consumer-groups.sh --delete --group <g>`, or `--delete-offsets --group <g> --topic orders.v1` for a shared group (one group at a time).
- Remove ACLs: `kafka-acls.sh --remove --topic orders.v1`.
- Remove the topic from any topic-as-code definitions or tooling that would recreate it.
- If you recreate a topic with the same name right away, restart long-lived clients if they keep reporting errors about the old topic.

## Verify
- [ ] `kafka-topics.sh --list` no longer shows it a minute later (and it did not come back).
- [ ] Disk freed on brokers (`kafka-log-dirs.sh`) after the delete delay.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: `delete.topic.enable` and `auto.create.topics.enable` defaults (both true, ServerConfigs source), `kafka-topics.sh --topic` accepting a regular expression except with `--create`, `--delete-offsets` semantics, the 60000 ms delete-delay default (ServerLogConfigs), `kafka-log-dirs.sh --topic-list`, Streams internal-topic naming, and the `kafka-streams-application-reset.sh` options. Removed: the `awk` pipeline, the `-delete` directory naming, ZooKeeper "marked for deletion" history, the "group must be empty" rule, Schema Registry, Terraform, JulieOps and Strimzi remarks, and the UNKNOWN_TOPIC_ID claim.

Method: documentation only; no commands were run.
