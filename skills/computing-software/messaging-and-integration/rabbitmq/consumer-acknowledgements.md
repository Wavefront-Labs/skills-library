---
id: computing-software.messaging-and-integration.rabbitmq.consumer-acknowledgements
name: consumer-acknowledgements
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, consumer-acknowledgements, rmq-consumers]
level: practitioner
status: docs-checked
description: "Use manual acks, nacks and rejects so messages are removed only after processing succeeds."
sources:
  - https://www.rabbitmq.com/docs/confirms
  - https://www.rabbitmq.com/docs/consumers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consumer acknowledgements

**Goal:** Get at-least-once processing.

## Steps
1. Consume with auto_ack=false; call basic.ack after the work is durable.
2. basic.nack or basic.reject with requeue=false sends to the DLX if configured; requeue=true returns it to the queue.
3. Acknowledge on the same channel that received the delivery.
4. The consumer acknowledgement timeout (default 30 minutes, set with `consumer_timeout` in milliseconds) closes the channel with a `PRECONDITION_FAILED` channel exception when a delivery is not acknowledged in time; checked at one-minute intervals. Starting with RabbitMQ 4.3, delivery acknowledgement timeouts are supported only by quorum queues.

## Failure modes
- Acking on a different channel than the delivery arrived on gives an "unknown delivery tag" protocol exception and closes the channel.
- Auto-ack loses messages if the consumer crashes.

## Verify
- Kill the consumer before acking and see the message return to Ready in `rabbitmqctl list_queues name messages_ready messages_unacknowledged`.

## Checked

Date: 2026-11-02. Confirmed in the Confirms guide (docs/confirms) and Consumers guide (docs/consumers): same-channel rule, requeue field, 30-minute default, `consumer_timeout`, `PRECONDITION_FAILED` on timeout. Corrected: the unknown-delivery-tag error is a separate protocol exception from the timeout's `PRECONDITION_FAILED`.

Method: documentation only; no commands were run.
