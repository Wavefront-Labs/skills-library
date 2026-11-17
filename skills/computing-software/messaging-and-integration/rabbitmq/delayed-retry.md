---
id: computing-software.messaging-and-integration.rabbitmq.delayed-retry
name: delayed-retry
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, delayed-retry]
level: advanced
status: docs-checked
description: "Delay retries using quorum queue delayed retry, a TTL queue with DLX loop, or the (unmaintained) delayed message exchange plugin."
sources:
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://www.rabbitmq.com/docs/dlx
  - https://www.rabbitmq.com/docs/ttl
  - https://www.rabbitmq.com/docs/quorum-queues
  - https://github.com/rabbitmq/rabbitmq-delayed-message-exchange
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delayed retry

**Goal:** Retry with backoff.

## Steps
1. Preferred on RabbitMQ 4.3 and later: quorum queue delayed retry with linear back-off. Set `x-delayed-retry-type` (`disabled` default, `all`, `failed` or `returned`), `x-delayed-retry-min` (required when enabled) and optionally `x-delayed-retry-max` in milliseconds, or the policy keys `delayed-retry-type`, `delayed-retry-min`, `delayed-retry-max`. Delay is `min(min_delay * delivery_count, max_delay)`. `delivery-count` rises only on failures, so a `returned` message may not be delayed longer than the minimum.
2. Otherwise use a dead-letter cycle: a retry queue (for example `retry.5s`) with `x-message-ttl` 5000 and a DLX pointing back to the main exchange. Add one queue per delay tier for coarse backoff.
3. The delayed message exchange plugin (`x-delayed-message` exchange type, `x-delayed-type` argument, `x-delay` header in milliseconds) is no longer maintained by the RabbitMQ team; its README recommends quorum queue delay or dead lettering instead.

## Failure modes
- Per-message TTLs in one queue: expired messages wait behind non-expired ones until they reach the head, so use one TTL per queue.
- Plugin: delayed messages live in a single-node Mnesia table, are lost if the plugin is disabled or the node is lost, the `mandatory` flag is unsupported, and it is intended for delays of seconds to hours, a day or two at most.

## Verify
- Observe redelivery timing.

## Checked
2026-11-09. Confirmed against the Quorum Queues page (delayed retry section: availability from 4.3, argument and policy names, retry types, delay formula, delivery-count note), the TTL page (expired messages queue behind non-expired ones and are discarded at the head), the Dead Letter Exchanges page (delayed-retry cycle description and recommendation of quorum delayed retry), and the delayed message exchange README (no longer maintained, `x-delayed-message`, `x-delayed-type`, `x-delay`, single-node Mnesia storage, no `mandatory`, delay range guidance). Removed: unsourced "limits apply" wording and the version note.
Method: documentation only; no commands were run.
