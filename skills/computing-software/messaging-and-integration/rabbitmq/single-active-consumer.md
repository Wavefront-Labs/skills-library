---
id: computing-software.messaging-and-integration.rabbitmq.single-active-consumer
name: single-active-consumer
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, single-active-consumer, rmq-consistency]
level: advanced
status: docs-checked
description: "Guarantee ordered processing with x-single-active-consumer so only one consumer receives at a time."
sources:
  - https://www.rabbitmq.com/docs/consumers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single active consumer

**Goal:** Keep order with failover.

## Steps
1. Declare with `x-single-active-consumer=true`.
2. The first registered consumer becomes the active one and the others are ignored; if it is cancelled or dies, another consumer is selected. On quorum queues, a consumer that registers with a higher priority takes over after the current one's messages are acknowledged.
3. Available on classic and quorum queues to AMQP 1.0 and AMQP 0-9-1 clients. On a stream it does not work through AMQP 0-9-1; use a native stream protocol client.

## Failure modes
- Throughput limited to a single consumer.

## Verify
- Stop the active consumer and watch a standby take over.

## Checked

Date: 2026-11-02. Confirmed in the Consumers guide (docs/consumers, Single Active Consumer section): the `x-single-active-consumer` argument, failover, priority takeover on quorum queues, stream restriction. Corrected: SAC on streams is not available to AMQP 0-9-1 clients.

Method: documentation only; no commands were run.
