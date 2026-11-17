---
id: computing-software.messaging-and-integration.rabbitmq.prefetch-qos
name: prefetch-qos
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, prefetch-qos]
level: practitioner
status: docs-checked
description: "Tune basic.qos prefetch to balance throughput against fairness and memory."
sources:
  - https://www.rabbitmq.com/docs/confirms
  - https://www.rabbitmq.com/docs/consumer-prefetch
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consumer prefetch

**Goal:** Stop one consumer hoarding messages.

## Steps
1. Set `basic.qos` `prefetch_count`; RabbitMQ applies it separately to each new consumer on the channel (the AMQP 0-9-1 spec says shared across the channel).
2. Values in the 100 to 300 range usually offer optimal throughput without overwhelming consumers; the best value is found by trial and error per workload.
3. Higher prefetch generally raises throughput but also consumer RAM use; unacknowledged deliveries are requeued when the channel closes.
4. A prefetch of `0` means no limit; use it with care, since consumers that do not acknowledge cause memory growth on the node. Quorum queues cap prefetch at 2,000.

## Failure modes
- Prefetch 1 is the most conservative and significantly reduces throughput, especially with high connection latency.
- Unlimited prefetch lets the number of delivered but unprocessed messages grow, increasing consumer RAM use.

## Verify
- Check `messages_unacknowledged` stays near consumers x prefetch.

## Checked

Date: 2026-11-02. Confirmed in the Confirms guide (docs/confirms, prefetch sections) and Consumer Prefetch guide (docs/consumer-prefetch). Corrected: the skill advised 10-50, but the guide says 100-300 usually gives optimal throughput. Removed: `global=false` wording and the redelivery-cost claim.

Method: documentation only; no commands were run.
