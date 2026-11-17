---
id: computing-software.messaging-and-integration.apache-pulsar.acknowledgment-and-negative-ack
name: acknowledgment-and-negative-ack
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [acknowledgment, negative-ack, ack-timeout, redelivery-backoff, cumulative-ack]
level: practitioner
status: docs-checked
description: "Acknowledge Pulsar messages individually or cumulatively, nack with redelivery delay and backoff, use ackTimeout, and avoid the in-memory nack counter trap."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/concepts-messaging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose the right acknowledgment mechanism so messages are deleted only after they are processed.

Ack basics: a consumer acks after successful consumption, and a message is removed from storage only after every subscription has acked it. Individual ack uses `consumer.acknowledge(msg)`. Cumulative ack uses `consumer.acknowledgeCumulative(msg)`, which acks that message and everything before it; it cannot be used with Shared or Key_Shared subscriptions, so use individual acks there.

Negative ack: `consumer.negativeAcknowledge(message)` asks the broker to redeliver. The default `negativeAckRedeliveryDelay` is 1 minute; set a shorter one with `.negativeAckRedeliveryDelay(2, TimeUnit.SECONDS)` on the consumer builder. For growing delays use `.negativeAckRedeliveryBackoff(MultiplierRedeliveryBackoff.builder().minDelayMs(1000).maxDelayMs(60 * 1000).multiplier(2).build())`, which gives 1, 2, 4 ... 60 seconds. Nacking a message inside a batch redelivers the whole batch.

Ack timeout: disabled by default, so an unacked message is only redelivered if the consumer disconnects. Enable it with `.ackTimeout(10, TimeUnit.SECONDS)` on the builder. Related options: `ackTimeoutTickTime` (how often expiry is checked) and `ackTimeoutRedeliveryBackoff` (growing redelivery delay). Prefer nack to ackTimeout when the consumer knows processing failed.

Gotcha: the nack redelivery counter is held only in memory, so it resets on broker restart, topic or bundle unload, or consumer disconnect. A `DeadLetterPolicy` with `maxRedeliverCount` driven by nacks may therefore never trigger. For a reliable retry limit use `reconsumeLater` with `enableRetry(true)` (see the retry-letter skill).

Verify: nack a message and confirm it returns after the configured delay; ack it and confirm it does not return.

## Checked

2026-11-03. Confirmed against the Pulsar messaging concepts page: individual and cumulative ack (not for Shared or Key_Shared), `negativeAckRedeliveryDelay` default 1 min, redelivery backoff, whole-batch redelivery, `ackTimeout` default 0 with `ackTimeoutTickTime` and `ackTimeoutRedeliveryBackoff`, nack preferred over ack timeout, in-memory nack counter reset events, and `reconsumeLater` with `enableRetry(true)` as the reliable retry limit.

Method: documentation only; no commands were run.
