---
id: computing-software.messaging-and-integration.rabbitmq.maintenance-mode
name: maintenance-mode
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, maintenance-mode, rmq-maintenance]
level: advanced
status: docs-checked
description: "Drain a node with rabbitmq-upgrade drain before restart so clients and leaders move."
sources:
  - https://www.rabbitmq.com/docs/upgrade
  - https://www.rabbitmq.com/docs/man/rabbitmq-upgrade.8
  - https://www.rabbitmq.com/docs/man/rabbitmq-diagnostics.8
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Maintenance mode

**Goal:** Restart a node without surprises.

## Steps
1. `rabbitmq-upgrade drain` puts the node in maintenance mode (it serves no client traffic and is not considered for hosting queue leaders); do the work; `rabbitmq-upgrade revive` brings it back.
2. Before stopping a node, check `rabbitmq-diagnostics check_if_node_is_quorum_critical`; `rabbitmq-upgrade await_online_quorum_plus_one` waits until stopping the node would not cost any queue its quorum.
3. In a rolling upgrade, nodes are upgraded one by one.

## Failure modes
- Stopping a node that makes a queue lose quorum.

## Verify
- Client connections and queue leaders are off the drained node.

## Checked

2026-11-02. Confirmed in the rabbitmq-upgrade man page: drain, revive, await_online_quorum_plus_one semantics; docs/upgrade: maintenance mode, nodes upgraded one by one; check_if_node_is_quorum_critical in the rabbitmq-diagnostics man page.
Method: documentation only; no commands were run.
