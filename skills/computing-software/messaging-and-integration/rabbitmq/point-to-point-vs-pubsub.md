---
id: computing-software.messaging-and-integration.rabbitmq.point-to-point-vs-pubsub
name: point-to-point-vs-pubsub
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, point-to-point-vs-pubsub, rmq-eip-channels]
level: intro
status: docs-checked
description: "Choose between point-to-point (competing consumers on one queue) and publish-subscribe (queue per subscriber) channels."
sources:
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://www.rabbitmq.com/docs/exchanges
  - https://www.rabbitmq.com/docs/queues
  - https://www.rabbitmq.com/docs/consumers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Point-to-point versus publish-subscribe

**Goal:** Map EIP channels to RabbitMQ.

## Steps
1. Point-to-point: one queue, several consumers share the work (round-robin dispatch limited by prefetch).
2. Publish-subscribe: a fanout exchange (a copy to every bound queue) or a topic exchange (routing key pattern match), with one queue per subscriber.
3. For messages that must survive a broker restart, use durable queues and publish messages as persistent; transient messages are discarded on recovery even in durable queues.

## Failure modes
- Sharing one queue across different subscribers makes them steal messages from each other.

## Verify
- Send 10 messages; consumer counts sum to 10 for point-to-point, and each subscriber sees 10 for publish-subscribe.

## Checked
2026-11-09. Point-to-Point and Publish-Subscribe channels are EIP patterns. Confirmed on the RabbitMQ Exchanges page (fanout copy to every bound queue, topic pattern matching), the Queues page (durable queues recovered on boot, transient messages discarded on recovery even in durable queues, persistent publishing needed) and the Consumers page (round-robin dispatch). Removed: the unqualified "durable queues for guaranteed delivery" (durability alone does not guarantee delivery) and the version note.
Method: documentation only; no commands were run.
