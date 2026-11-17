---
id: computing-software.messaging-and-integration.rabbitmq.quorum-queue-basics
name: quorum-queue-basics
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, quorum-queue-basics, rmq-quorum-queues]
level: practitioner
status: docs-checked
description: "Declare quorum queues (Raft replicated) and understand their durability, quorum requirement and what is not supported."
sources:
  - https://www.rabbitmq.com/docs/quorum-queues
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quorum queue basics

**Goal:** Get replicated, durable queues with predictable failover.

## Steps
1. Declare with `x-queue-type=quorum`. Quorum queues are always durable and cannot be exclusive.
2. A majority of members, `(N/2)+1`, must agree and be online.
3. Group size is up to three members by default; `x-quorum-initial-group-size` changes it. Use an odd group size; three is the smallest practical value and tolerates one node failure.
4. Quorum queues support strict message priorities (32 levels) from RabbitMQ 4.3; earlier versions mapped priorities onto two buckets.

## Failure modes
- Losing a majority of replicas leaves the queue without an online majority until quorum returns.
- Quorum queues do not support global QoS prefetch.

## Verify
- `rabbitmq-queues quorum_status <queue>` shows leader and followers.

## Checked

Date: 2026-11-02. Confirmed on the Quorum Queues guide: durability, no exclusive, majority formula, default group size of three, odd sizes, priorities by version, global QoS, `quorum_status`. Removed: auto-delete, the "recommended replicated queue type" line, the unconfirmed-features note.

Method: documentation only; no commands were run.
