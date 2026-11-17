---
id: computing-software.messaging-and-integration.rabbitmq.scatter-gather
name: scatter-gather
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, scatter-gather]
level: advanced
status: docs-checked
description: "Broadcast a request to several services and gather replies on a reply queue within a deadline."
sources:
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://www.rabbitmq.com/docs/direct-reply-to
  - https://www.rabbitmq.com/docs/exchanges
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scatter-gather

**Goal:** Query many workers in parallel.

## Steps
1. Publish the request to a fanout or topic exchange (a fanout routes a copy to every bound queue; a topic exchange matches on the routing key pattern) with `reply_to` and `correlation_id` set.
2. Collect replies on a reply queue until a deadline. An exclusive queue deleted on disconnect suits a single requester, and `x-expires` can clean up reply queues that are never drained. Direct reply-to (`amq.rabbitmq.reply-to`) needs no queue but requires no-ack consumption on the same channel that publishes, and its replies are dropped if the requester disconnects.
3. Treat replies arriving after the deadline as dropped.

## Failure modes
- Waiting for all replies blocks on the slowest worker.
- A reply queue that outlives the requester collects stale replies.

## Verify
- Measure the time until the deadline with one worker offline.

## Checked
2026-11-09. Confirmed against the Direct Reply-to page (exclusive reply queues, `amq.rabbitmq.reply-to`, same channel requirement, `correlation-id`), the Time-to-Live page (`x-expires` for RPC-style reply queues) and the Exchanges page (fanout and topic semantics). Removed: the version note.
Method: documentation only; no commands were run.
