---
id: computing-software.messaging-and-integration.rabbitmq.at-least-once-delivery
name: at-least-once-delivery
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, at-least-once-delivery, rmq-reliability]
level: advanced
status: docs-checked
description: "Combine durable queues, persistent messages, confirms and manual acks for at-least-once and make consumers idempotent."
sources:
  - https://www.rabbitmq.com/docs/confirms
  - https://www.rabbitmq.com/docs/queues
  - https://www.rabbitmq.com/docs/quorum-queues
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# At-least-once delivery

**Goal:** Reduce the chance of loss end to end.

## Steps
1. Use a durable queue, persistent messages (see the queues guide on durability and message persistence), publisher confirms, and manual consumer acknowledgements.
2. Automatic acknowledgement is unsafe: a message sent to a consumer whose connection or channel closes before delivery succeeds is lost.
3. Requeued or redelivered messages happen; consumers should tolerate duplicates (for example by tracking a message id) and may track redelivery counts to avoid redelivery loops.
4. Acknowledge only after the work is done.

## Failure modes
- Skipping any link (non-durable queue, no confirms, auto-ack) reintroduces loss.
- Non-idempotent handlers duplicate effects on redelivery.

## Verify
- Restart a node under load and compare messages sent with distinct messages processed.

## Checked

2026-11-02. Confirmed in docs/confirms: manual acks versus automatic acknowledgement loss, redelivery loops and redelivery tracking, publisher confirms; docs/queues: durable queues. Removed: the "exactly-once is not provided" line (not stated in pages) and the specific delivery_mode 2 requirement.
Method: documentation only; no commands were run.
