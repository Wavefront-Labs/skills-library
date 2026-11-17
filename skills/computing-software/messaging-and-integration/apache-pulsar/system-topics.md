---
id: computing-software.messaging-and-integration.apache-pulsar.system-topics
name: system-topics
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [system-topics, change-events, transaction-log, heartbeat, topic-level-policies, include-system-topic]
level: practitioner
status: docs-checked
description: "Recognise Pulsar system topics (__change_events, transaction logs, heartbeat, resource-usage), list them with --include-system-topic, and enable them before 2.11."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/concepts-messaging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know what the predefined internal topics are so you do not delete or misread them.

System topics implement features inside Pulsar without third-party dependencies: transactions, heartbeat detection, topic-level policies and the resource group service. Per namespace:
- `pulsar/system`: `transaction_coordinator_assign_${id}` (persistent, default 16) for the transaction coordinator; `__transaction_log_${tc_id}` (persistent, default 16) for the transaction log; `resource-usage` (non-persistent, default 4) for the resource group service.
- `host/port` namespace: `heartbeat` (persistent, 1) for heartbeat detection.
- User namespaces: `__change_events` (persistent, default 4) carries topic events and topic-level policies; `__transaction_buffer_snapshot` (persistent, one per namespace) holds transaction buffer snapshots; `${topicName}__transaction_pending_ack` (persistent) exists once per topic subscription that acknowledges with transactions.

Rules:
- You cannot create system topics yourself.
- To see them in a topic listing, add the option `--include-system-topic` when listing via the Pulsar admin tool.
- Since Pulsar 2.11.0 system topics are enabled by default. In earlier versions set these in `conf/broker.conf` or `conf/standalone.conf`:
```properties
systemTopicEnabled=true
topicLevelPoliciesEnabled=true
```

Gotcha: topic-level policies stop working if the system topic mechanism is disabled on a pre-2.11 broker.

Verify: list topics of a namespace with and without `--include-system-topic` and confirm `__change_events` appears only with it.

## Checked

2026-11-03. Confirmed against the Pulsar messaging concepts page, system topics section: the topic table (namespace, persistence, default counts), the cannot-create rule, `--include-system-topic`, enabled by default since 2.11.0 and the two broker.conf/standalone.conf settings for earlier versions.

Method: documentation only; no commands were run.
