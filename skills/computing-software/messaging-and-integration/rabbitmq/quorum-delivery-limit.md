---
id: computing-software.messaging-and-integration.rabbitmq.quorum-delivery-limit
name: quorum-delivery-limit
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, quorum-delivery-limit]
level: practitioner
status: docs-checked
description: "Cap redelivery loops on quorum queues with delivery-limit and send poison messages to a dead letter exchange."
sources:
  - https://www.rabbitmq.com/docs/quorum-queues
  - https://www.rabbitmq.com/docs/dlx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quorum delivery limit

**Goal:** Stop poison messages from looping forever.

## Steps
1. Set a policy: `rabbitmqctl set_policy dl-limit "^work\." '{"delivery-limit":5}' --apply-to queues`. It can also be the `x-delivery-limit` queue argument; `-1` disables the limit, which the guide advises against.
2. A message redelivered more times than the limit is dropped, or dead-lettered if a DLX is configured. The guide recommends a dead letter configuration on every quorum queue.
3. Since RabbitMQ 4.0 the default limit is 20 (3.13.x had none).

## Failure modes
- Without a DLX, over-limit messages are discarded.
- With prefetch above 1, all outstanding unacknowledged deliveries can be discarded together if they were requeued as a group.
- What counts depends on version: from 4.3 the limit uses `delivery-count`, which `basic.reject` and client crash or connection loss increment but `basic.nack` and consumer timeout do not.

## Verify
- Redelivered messages carry the `x-delivery-count` header; an AMQP 0.9.1 message dead-lettered by the DLX carries an `x-death` header.

## Checked

Date: 2026-11-02. Confirmed on the Quorum Queues guide (Poison Message Handling, delivery-count table) and the Dead Letter Exchanges guide: policy key, -1, default 20 from 4.0, drop or dead-letter, headers. Fixed: "nack with requeue counts toward the limit" is wrong from 4.3. Removed: the generic "check your version" step.

Method: documentation only; no commands were run.
