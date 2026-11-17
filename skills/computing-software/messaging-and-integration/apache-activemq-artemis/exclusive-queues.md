---
id: computing-software.messaging-and-integration.apache-activemq-artemis.exclusive-queues
name: exclusive-queues
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,exclusive-queues,exclusive,default-exclusive-queue,activemq-artemis,ordering]
level: practitioner
status: docs-checked
description: "Make a queue dispatch to one consumer at a time with exclusive=true, a JMS address parameter or the default-exclusive-queue address-setting."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/exclusive-queues.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exclusive queues

**Goal:** guarantee that all messages on a queue go to a single consumer at a time, so they are processed strictly in the order produced, when message grouping is not usable.

## Configure
Static queue in `broker.xml`:
```xml
<address name="foo.bar">
   <multicast>
      <queue name="orders1" exclusive="true"/>
   </multicast>
</address>
```
Other routes to the same flag: pass `exclusive` = `true` to the Core API when creating the queue, or use an address parameter on auto-created JMS destinations:
```java
Queue queue = session.createQueue("my.destination.name?exclusive=true");
Topic topic = session.createTopic("my.destination.name?exclusive=true");
```
To default every queue under an address, set `default-exclusive-queue` to `true` in an `address-setting` (the default is `false`). Address wildcards in `match` let one setting cover a set of addresses.

## Trade-off
Only one consumer is technically active, so you cannot scale out consumption. The manual advises trying message groups first (see `message-grouping`) and using an exclusive queue only when you cannot or do not want grouping, for example orders that must be consumed in exactly the produced order.

## Verify
Attach two consumers to the queue, send a numbered series of messages, and confirm only one consumer receives them, in order.

## Checked
Method: docs-checked 2026-11-09 against the raw exclusive-queues.adoc source (read in full); broker.xml, Core API, JMS parameter and default-exclusive-queue details match.
