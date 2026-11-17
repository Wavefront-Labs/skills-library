---
id: computing-software.messaging-and-integration.strimzi.upgrade-sequence
name: upgrade-sequence
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [strimzi-upgrade, upgrade-order, kraft-required]
level: sme
status: docs-checked
description: "Follow the required order to upgrade Strimzi, Kafka and clients."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Required upgrade sequence

**Goal:** upgrade without downtime.

Order:

1. Confirm your Kubernetes version is supported. Strimzi 1.3.0 requires Kubernetes 1.32 or later; you can upgrade Kubernetes with minimal downtime.
2. Ensure Kafka clusters are KRaft-based. If upgrading from a version earlier than 0.39, migrate from ZooKeeper to KRaft **before** upgrading the Cluster Operator; upgrades from ZooKeeper-based clusters are not supported.
3. Prepare for the v1 API conversion. From versions earlier than 0.49 this includes a `KafkaUser` update done before upgrading the Cluster Operator.
4. Upgrade the Cluster Operator.
5. Update the Kafka version and `metadataVersion`.

From Strimzi 0.39, upgrades and downgrades between KRaft-based clusters are supported.

Related guide sections: upgrading from versions earlier than 1.0.0, checking upgrade status, upgrade paths, strategies for upgrading clients, and downgrading.

After upgrading, check the `kafkaVersion` and `operatorLastSuccessfulVersion` values in the `status` of the `Kafka` resource.

**Checklist**

1. Migrate to KRaft first when old.
2. Convert APIs to `v1`.
3. Upgrade operator, then Kafka, then clients.

## Checked

2026-11-03. Confirmed in Required upgrade sequence: Kubernetes 1.32 or later for Strimzi 1.3.0, KRaft requirement and the pre-0.39 migration, v1 API conversion (KafkaUser update before 0.49), and the related section list. Replaced the unconfirmed jsonpath status.kafkaVersion command with the documented kafkaVersion and operatorLastSuccessfulVersion status values.

Method: documentation only; no commands were run.
