---
id: computing-software.messaging-and-integration.apache-activemq-artemis.scheduled-messages
name: scheduled-messages
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,scheduled-messages,amq-sched-delivery,delayed-delivery,hdr-scheduled-delivery-time,activemq-artemis]
level: intro
status: docs-checked
description: "Delay delivery by setting the _AMQ_SCHED_DELIVERY long property to an absolute epoch time in milliseconds on the message before sending."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/scheduled-messages.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled messages

**Goal:** make a message undeliverable until a given time in the future.

A scheduled message is an ordinary message carrying the property `_AMQ_SCHED_DELIVERY` (the constant `Message.HDR_SCHEDULED_DELIVERY_TIME`). Its value must be a positive `long`: the earliest delivery time in milliseconds, not a delay. The broker will not deliver the message before that time.

## JMS example
```java
TextMessage message = session.createTextMessage("This is a scheduled message which will be delivered in 5 sec.");
message.setLongProperty("_AMQ_SCHED_DELIVERY", System.currentTimeMillis() + 5000);
producer.send(message);

TextMessage messageReceived = (TextMessage) consumer.receive();
```
The Core API works the same way: set the same property on the core message before sending.

## Notes
- The value is an absolute time, so compute `System.currentTimeMillis() + delayMs`, as the manual's example does.
- The manual says only "at the earliest": do not assume exact-time delivery.

## Checked
2026-11-03. Confirmed against the Artemis user manual page scheduled-messages: property name and constant, positive long, JMS example, Core API. Removed: the Verify step and a clock-skew claim.
Method: documentation only; no commands were run.
