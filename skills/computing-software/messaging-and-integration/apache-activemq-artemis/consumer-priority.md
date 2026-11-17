---
id: computing-software.messaging-and-integration.apache-activemq-artemis.consumer-priority
name: consumer-priority
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,consumer-priority,priority,round-robin,activemq-artemis,openwire,amqp]
level: practitioner
status: docs-checked
description: "Prefer high-priority consumers using the consumer-priority address parameter (Core), consumer.priority (OpenWire) or the AMQP attach priority property."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/consumer-priority.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consumer priority

**Goal:** make high-priority consumers get messages while they are active, falling back to lower ones only when needed.

Without priorities, active consumers on a queue receive messages round-robin. With priorities, round-robin applies only among consumers sharing the highest priority. Lower-priority consumers receive messages only when the high-priority ones have no credit, or have declined the message (for example because it does not match their selector). An unset priority is `0`.

## Core / JMS
```java
Queue queue = session.createQueue("my.destination.name?consumer-priority=50");
consumer = session.createConsumer(queue);
```
Range: -2^31 to 2^31-1.

## OpenWire
```java
queue = new ActiveMQQueue("TEST.QUEUE?consumer.priority=10");
```
Because of OpenWire limits the range is 0 to 127, with 127 highest.

## AMQP 1.0
Set the key `priority` (literal string) in the properties map of the attach frame, where the broker is the sending side of the link. Value is an integer in -2^31 to 2^31-1.

## Verify
Attach a priority-50 and a priority-0 consumer, send messages, and confirm the priority-50 consumer takes them until its credit is exhausted.

## Checked
Method: docs-checked 2026-11-09 against the raw consumer-priority.adoc source (read in full); behaviour, address parameters, ranges and AMQP attach property match.
