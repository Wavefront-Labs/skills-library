---
id: computing-software.messaging-and-integration.rabbitmq.competing-consumers
name: competing-consumers
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, competing-consumers]
level: practitioner
status: docs-checked
description: "Scale processing with several consumers on one queue and prefetch for fair dispatch."
sources:
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://www.rabbitmq.com/docs/consumers
  - https://www.rabbitmq.com/docs/consumer-prefetch
  - https://www.rabbitmq.com/docs/confirms
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Competing consumers

**Goal:** Scale out a work queue.

## Steps
1. Start N consumers on one queue. Without Single Active Consumer, messages are dispatched round-robin to consumers, limited by each consumer's effective prefetch.
2. Set a per-consumer prefetch with `basic.qos`; RabbitMQ applies `prefetch_count` separately to each new consumer on the channel (unlike the AMQP 0-9-1 text, where it is shared), and 0 means unlimited. Tune the value to message cost; a default can be set with `default_consumer_prefetch` in the advanced config file.
3. Use manual acknowledgements. Unacked deliveries are requeued when the channel or connection closes, so handlers must tolerate redelivery (the `redeliver` property is true on redeliveries).
4. Use Single Active Consumer (`x-single-active-consumer` true, set at declaration, not by policy) when processing order matters: only one consumer receives messages and another takes over if it is cancelled or dies.

## Failure modes
- Message ordering is lost with several active consumers.
- An unlimited prefetch lets one consumer hoard messages.

## Verify
- Watch deliveries spread across consumers with `rabbitmqctl list_consumers` or the management UI.

## Checked
2026-11-09. Confirmed against the Consumers page (round-robin, Single Active Consumer behaviour and declaration-only argument, `list_consumers`), the Consumer Prefetch page (per-consumer semantics, 0 as unlimited, `default_consumer_prefetch`) and the Acknowledgements page (automatic requeueing, `redeliver`). Removed: the "prefetch 1-10" figure, which no page recommends, and the version note.
Method: documentation only; no commands were run.
