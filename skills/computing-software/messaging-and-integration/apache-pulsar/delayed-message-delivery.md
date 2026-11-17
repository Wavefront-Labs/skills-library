---
id: computing-software.messaging-and-integration.apache-pulsar.delayed-message-delivery
name: delayed-message-delivery
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [delayed-delivery, deliver-after, delayed-delivery-tick-time, delayed-delivery-tracker, backlog-quota]
level: practitioner
status: docs-checked
description: "Schedule Pulsar messages with deliverAfter on Shared or Key_Shared subscriptions and tune broker delayedDelivery settings; interactions with retention, quota and TTL."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/concepts-messaging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: deliver a message to consumers at a later time.

Mechanism: the message is stored in BookKeeper like any other. The broker keeps a time index (time to message id) in memory in the `DelayedDeliveryTracker`, and the subscription fetches messages from it once their delay elapses. Only Shared and Key_Shared subscriptions support delay; on any other subscription type delayed messages are dispatched immediately.

Producer (Java): `producer.newMessage().deliverAfter(3L, TimeUnit.MINUTES).value("Hello Pulsar!").send();`

Broker settings in `broker.conf` (enabled by default):
- `delayedDeliveryEnabled=true`: if false, messages are delivered immediately with no tracking overhead.
- `delayedDeliveryTickTimeMillis=1000`: tick time of the HashedWheelTimer used by the default in-memory tracker; affects accuracy of delivery versus schedule.
- `isDelayedDeliveryDeliverAtTimeStrict=false`: when false, messages may go out up to one tick early; when true they never go before deliverAt but can be late by the tick times.
- `maxNumDelayedDeliveryTrackerMemoryEntries=100000`: limit of delayed messages per dispatcher; beyond it no more delayed messages are allowed.

Interactions with other policies:
- Retention: Pulsar deletes the front ledgers of a topic, never ledgers in the middle, so a message with a very long delay can keep storage pinned.
- Backlog quota: delayed messages stay unconsumed for a long time and can trigger the backlog quota policy, blocking later sends, so apply quotas carefully.
- Backlog TTL: when the TTL expires the message is acknowledged regardless of its delay.

## Checked

2026-11-03. Confirmed against the Pulsar messaging concepts page, delayed delivery section: Shared and Key_Shared only, `deliverAfter`, the four broker.conf settings and defaults, and the retention, backlog quota and backlog TTL interactions. Removed: the generic Verify line.

Method: documentation only; no commands were run.
