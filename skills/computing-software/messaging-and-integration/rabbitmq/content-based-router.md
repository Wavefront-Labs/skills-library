---
id: computing-software.messaging-and-integration.rabbitmq.content-based-router
name: content-based-router
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, content-based-router, rmq-eip-routing]
level: practitioner
status: docs-checked
description: "Route messages by content using a producer-side key, topic or headers exchange."
sources:
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://www.rabbitmq.com/docs/exchanges
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Content-based router

**Goal:** Direct a message to the right queue by its content.

## Steps
1. Compute the routing key from the content (for example `type.region`) in the publisher.
2. Use a topic exchange so receivers bind by pattern (`*` for one word, `#` for zero or more), a direct exchange for exact keys, or a headers exchange to match on message headers set by the publisher.
3. Do not make the broker read the body: RabbitMQ exchanges route on the routing key or headers, not the payload, so any body-based decision belongs in the publisher or a router consumer.
4. Give unroutable messages somewhere to go: an alternate exchange, or the `mandatory` flag to get returns; otherwise unroutable messages are dropped.

## Failure modes
- Reading the body in a consumer router adds a hop and latency.

## Verify
- Publish sample types and check queue arrival.

## Checked
2026-11-09. Content-based Router is named on the EIP messaging index. Confirmed on the RabbitMQ Exchanges page: topic pattern matching on the routing key, `#` matching any key, direct exchange exact match, headers exchange using exchange arguments. Confirmed on the Publishers page: unroutable messages are discarded or sent to an alternate exchange when `mandatory` is false, and returned when it is true. Removed: the version note.
Method: documentation only; no commands were run.
