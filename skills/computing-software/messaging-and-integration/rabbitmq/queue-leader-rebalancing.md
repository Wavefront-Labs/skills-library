---
id: computing-software.messaging-and-integration.rabbitmq.queue-leader-rebalancing
name: queue-leader-rebalancing
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, queue-leader-rebalancing]
level: advanced
status: docs-checked
description: "Rebalance queue leaders across nodes after restarts for even load."
sources:
  - https://www.rabbitmq.com/docs/man/rabbitmq-queues.8
  - https://www.rabbitmq.com/docs/clustering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue leader rebalancing

**Goal:** Spread queue leaders across nodes.

## Steps
1. `rabbitmq-queues rebalance all` (types: all, quorum, classic, stream; optionally `--vhost-pattern` and `--queue-pattern`).
2. Set the queue leader locator: `client-local` (the default; picks the node the client is connected to) or `balanced` (considers how many leaders each node already has). Configure it via policy `queue-leader-locator` or the `queue_leader_locator` setting.
3. Do it at a quiet time, since leaders move.

## Verify
- Compare the leader node of your queues before and after (management UI queue list).

## Checked

2026-11-02. Confirmed in the rabbitmq-queues man page: rebalance types and patterns; docs/clustering: client-local and balanced locators, policy and config names. Removed: `list_queues name leader` (no `leader` info item found in the man page) and the post-rolling-restart claim.
Method: documentation only; no commands were run.
