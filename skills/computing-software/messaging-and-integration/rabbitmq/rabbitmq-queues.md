---
id: computing-software.messaging-and-integration.rabbitmq.rabbitmq-queues
name: rabbitmq-queues
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, rabbitmq-queues]
level: advanced
status: docs-checked
description: "Use rabbitmq-queues to manage quorum queue membership, rebalance leaders and inspect status."
sources:
  - https://www.rabbitmq.com/docs/man/rabbitmq-queues.8
  - https://www.rabbitmq.com/docs/quorum-queues
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rabbitmq-queues

**Goal:** Maintain quorum queue replicas.

## Steps
1. `rabbitmq-queues quorum_status <queue>`, `add_member`, `delete_member`, `rebalance <type>`.
2. `grow <node> <selector>` adds replicas on a new node; `shrink <node>` removes them when a node is decommissioned.

## Failure modes
- Rebalancing moves queue leader replicas across nodes, which can briefly interrupt traffic on the moved queues.

## Verify
- `quorum_status` lists the new member.

## Checked

Date: 2026-11-02. Confirmed on the rabbitmq-queues man page: command names and `rebalance` semantics. Removed: "rebalance after rolling restarts", "new member shown as follower" and the blip claim beyond leader movement.

Method: documentation only; no commands were run.
