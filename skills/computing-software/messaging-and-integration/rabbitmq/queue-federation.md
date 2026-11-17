---
id: computing-software.messaging-and-integration.rabbitmq.queue-federation
name: queue-federation
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, queue-federation]
level: advanced
status: docs-checked
description: "Move messages between sites on demand by federating queues so remote consumers can pull when local consumers are idle."
sources:
  - https://www.rabbitmq.com/docs/federated-queues
  - https://www.rabbitmq.com/docs/federation
  - https://www.rabbitmq.com/docs/federation-reference
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue federation

**Goal:** Balance work between brokers.

## Steps
1. Use the same `federation-upstream` definition as for exchanges; the policy uses `--apply-to queues`.
2. A federated queue retrieves messages from upstream queues to satisfy demand from local consumers; it prefers local consumers to remote ones and moves messages only if the upstream has no local consumers.
3. Messages are moved, not replicated.

## Failure modes
- Messages can be reordered across a set of mutually federated queues.
- Federated queues move load around; they are not a replication mechanism.

## Verify
- Stop consumers at one site and confirm messages move to where consumers are connected.

## Checked

Date: 2026-11-02. Confirmed on the Federated Queues guide. Removed: "idle consumers" wording and "moves once" claim.

Method: documentation only; no commands were run.
