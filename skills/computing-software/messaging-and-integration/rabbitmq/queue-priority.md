---
id: computing-software.messaging-and-integration.rabbitmq.queue-priority
name: queue-priority
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, queue-priority, rmq-priority-length]
level: practitioner
status: docs-checked
description: "Declare classic priority queues with x-max-priority and publish a priority property; keep the priority range small."
sources:
  - https://www.rabbitmq.com/docs/priority
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Priority queues

**Goal:** Let urgent messages overtake.

## Steps
1. Declare a classic queue with `x-max-priority`, a positive integer in [1, 255]; 2 to 4 levels is highly recommended.
2. Set the message `priority` property (an unsigned byte, 0-255); higher is delivered first. Messages without it count as 0, and a priority above the queue maximum is treated as the maximum.
3. Delivery order is subject to consumer prefetch; with a high prefetch, lower priority messages can already be in flight.

## Failure modes
- Each priority level costs memory and disk per queue, plus CPU, especially when consuming.
- Quorum queues always support priorities, with 32 levels (0-31) from RabbitMQ 4.3 (earlier versions mapped priorities onto two buckets); `x-max-priority` is ignored by quorum queues.

## Verify
- Publish low then high priority and check consumption order with prefetch 1.

## Checked

Date: 2026-11-02. Confirmed in the Priority Queues page (docs/priority): ranges, recommendation, capping, resource cost, quorum queue behaviour in 4.3.

Method: documentation only; no commands were run.
