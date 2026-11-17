---
id: computing-software.messaging-and-integration.rabbitmq.rolling-upgrade
name: rolling-upgrade
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, rolling-upgrade, rmq-upgrades]
level: advanced
status: docs-checked
description: "Upgrade a cluster one node at a time with feature flags enabled and queue leaders drained."
sources:
  - https://www.rabbitmq.com/docs/upgrade
  - https://www.rabbitmq.com/docs/rolling-upgrade
  - https://www.rabbitmq.com/docs/feature-flags
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rolling upgrade

**Goal:** Upgrade with no downtime.

## Steps
1. Read the release notes and the upgrade guide for your path; the guide lists which versions have rolling-upgrade paths.
2. Enable all stable feature flags before upgrading: `rabbitmqctl enable_feature_flag all`.
3. Check no alarms are in effect and no replica sync is running. For each node: optionally `rabbitmq-upgrade drain` (maintenance mode), stop, upgrade RabbitMQ and, if applicable, Erlang, start, and watch monitoring and health checks before the next node.
4. After all nodes are upgraded, enable the new stable feature flags.

## Failure modes
- Unenabled stable feature flags can make the upgrade fail.
- Upgrading across a path not supported for rolling upgrades.

## Verify
- `rabbitmqctl cluster_status` and `rabbitmqctl list_feature_flags`.

## Checked

Date: 2026-11-02. Confirmed on the Upgrading and Rolling Upgrade guides and Feature Flags guide. Removed: "wait for sync" wording and "blocks the next upgrade".

Method: documentation only; no commands were run.
