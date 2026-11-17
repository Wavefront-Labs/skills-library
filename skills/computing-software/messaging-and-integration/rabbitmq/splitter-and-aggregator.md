---
id: computing-software.messaging-and-integration.rabbitmq.splitter-and-aggregator
name: splitter-and-aggregator
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, splitter-and-aggregator]
level: advanced
status: docs-checked
description: "Split a composite message into parts and aggregate replies using correlation id and a store."
sources:
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://www.rabbitmq.com/docs/dlx
  - https://www.rabbitmq.com/docs/confirms
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Splitter and aggregator

**Goal:** Process batches and recombine.

## Steps
1. The splitter publishes each part with a shared `correlation_id` and the total part count (for example in a header).
2. The aggregator consumes replies with manual acknowledgements, stores them keyed by `correlation_id`, and completes the group when all parts have arrived. Persist the group state, because unacked deliveries are requeued and redelivered if the aggregator disconnects (the `redeliver` property is true), so the aggregator must ignore duplicate parts.
3. Add a group timeout. Route incomplete groups to a parking queue; dead-letter exchanges apply to rejected or expired messages, not to an aggregator's own timeout, so publish the incomplete group explicitly.

## Failure modes
- Lost parts cause hanging aggregates; use timeouts.
- Redelivered parts counted twice if not deduplicated.

## Verify
- Send a batch of 5 and receive one aggregate.

## Checked
2026-11-09. Splitter and Aggregator confirmed as named patterns on the EIP messaging index. Confirmed on the RabbitMQ Acknowledgements page: unacked deliveries are requeued on channel or connection close and carry `redeliver` true. Confirmed on the Dead Letter Exchanges page: dead-lettering is triggered by reject or nack without requeue, TTL expiry, length limit or delivery limit. Removed: the original instruction to use a DLX for incomplete groups (a timeout in the aggregator is not a dead-lettering trigger) and the version note.
Method: documentation only; no commands were run.
