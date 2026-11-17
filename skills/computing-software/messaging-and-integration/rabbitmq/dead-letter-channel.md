---
id: computing-software.messaging-and-integration.rabbitmq.dead-letter-channel
name: dead-letter-channel
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, dead-letter-channel]
level: practitioner
status: docs-checked
description: "Implement the EIP dead letter channel with DLX plus a retry policy and a parking queue."
sources:
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://www.rabbitmq.com/docs/dlx
  - https://www.rabbitmq.com/docs/quorum-queues
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dead letter channel

**Goal:** Handle poison messages.

## Steps
1. Set `dead-letter-exchange` (and optionally `dead-letter-routing-key`) on the main queue by policy; prefer policies to hardcoded `x-dead-letter-exchange` arguments because policies can change without redeploying. The user needs read on the queue and write on the DLX.
2. Dead-lettering triggers: `basic.reject` or `basic.nack` with requeue false, per-message TTL expiry, a queue length limit drop, or exceeding a quorum queue `delivery-limit`. Expiry of a whole queue does not dead-letter its messages.
3. Retry loop: route the DLX to a retry queue with a message TTL whose own DLX points back to the main exchange. Count attempts from the `x-death` header (array, most recent first; each element has `queue`, `reason`, `count`); `reason` is one of `rejected`, `expired`, `maxlen`, `delivery_limit`.
4. After N tries, have the consumer publish to a parking queue (or use a quorum queue `delivery-limit` so the broker dead-letters poison messages to the parking DLX).
5. Alert on parking queue depth.

## Failure modes
- A dead-letter cycle with no rejection anywhere in it is detected and the message is dropped by RabbitMQ.
- If the DLX does not exist when needed, messages are silently dropped.
- Default dead-lettering is at-most-once and does not use publisher confirms internally; quorum queues offer `dead-letter-strategy` `at-least-once` (needs `overflow` set to `reject-publish`; with the default `drop-head` it falls back to at-most-once).

## Verify
- Force a failure and see it park after N tries.

## Checked
2026-11-09. Confirmed against the RabbitMQ Dead Letter Exchanges page (triggers, policy keys, permissions, `x-death` fields and reasons, cycle detection, missing DLX drops, at-most-once default) and the Quorum Queues page (`dead-letter-strategy` `at-least-once`, `drop-head` incompatibility). Pattern name confirmed on the EIP messaging index. Removed: the unsourced version note.
Method: documentation only; no commands were run.
