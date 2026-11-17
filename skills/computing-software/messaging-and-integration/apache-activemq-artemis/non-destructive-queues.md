---
id: computing-software.messaging-and-integration.apache-activemq-artemis.non-destructive-queues
name: non-destructive-queues
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,non-destructive,default-non-destructive,queue-browser,expiry-delay,activemq-artemis]
level: practitioner
status: docs-checked
description: "Create queues whose consumers never remove messages using non-destructive=true, and bound their growth with expiry-delay or a ring queue."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/non-destructive-queues.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Non-destructive queues

**Goal:** let consumers read messages without removing them, as a queue browser does, for every consumer of the queue.

Normally a consumer acquires messages exclusively and acknowledging deletes them. A non-destructive consumer behaves like a browser: it receives all messages, other consumers can still receive them, and acknowledgement does not remove them. When every consumer on a queue is non-destructive you get useful behaviours; on a last value queue the queue always holds the latest value for each key.

## Configure
Per queue in `broker.xml`:
```xml
<address name="foo.bar">
   <multicast>
      <queue name="orders1" non-destructive="true" />
   </multicast>
</address>
```
For auto-created JMS destinations use an address parameter:
```java
Queue queue = session.createQueue("my.destination.name?non-destructive=true");
```
To default all queues under an address, set `default-non-destructive` to `true` in an `address-setting` (default `false`).

## Bound the queue size
Outside last-value queues, messages never get deleted if all consumers are non-destructive, so the queue grows without limit. Set a default `expiry-delay` (see `message-expiry`) or use a ring queue (see `ring-queues`).

## Verify
Consume and acknowledge a message, then check the queue's message count in the console: it should be unchanged.

## Checked

Method: docs-checked 2026-11-09 against non-destructive-queues.adoc (read in full)
