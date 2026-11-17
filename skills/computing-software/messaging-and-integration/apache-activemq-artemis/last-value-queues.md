---
id: computing-software.messaging-and-integration.apache-activemq-artemis.last-value-queues
name: last-value-queues
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,last-value-queue,last-value-key,default-last-value-key,amq-lvq-name,lvq,activemq-artemis]
level: practitioner
status: docs-checked
description: "Keep only the newest message per key with last-value-key on a queue, default-last-value-key, or the legacy last-value flag using _AMQ_LVQ_NAME."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/last-value-queues.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Last-value queues

**Goal:** a queue that discards an older message when a newer one arrives with the same value of a chosen property (for example the latest price per stock). Messages without that property are delivered normally and never replaced.

## Configure
Static, in `broker.xml`:
```xml
<address name="foo.bar">
   <multicast>
      <queue name="orders1" last-value-key="reuters_code" />
   </multicast>
</address>
```
- Core API: create the queue with `lastValue` set to `true`.
- JMS auto-create: `session.createQueue("my.destination.name?last-value-key=reuters_code")`.
- Default for all queues under an address: `default-last-value-key` in an `address-setting` (default `null`).
- Legacy flag: `last-value="true"` on the queue (or `?last-value=true`, or `default-last-value-queue` true in an address-setting; the older `last-value-queue` setting is deprecated). The key then defaults to `_AMQ_LVQ_NAME` (constant `Message.HDR_LAST_VALUE_NAME`).

## Behaviour
Sending two messages with `setStringProperty("reuters_code", "VOD")` leaves only the second in the queue. It is common to combine this with non-destructive consumers (see `non-destructive-queues`).

## Clustering limit
Last-value queues are not supported in a traditional cluster: enforcing "last" needs all messages on one node, and redistribution would change which message is last. Use a connection router in front of the brokers so clients needing the same last-value queue reach the same node.

## Verify
Send two messages with the same key and confirm the queue count is 1 and the consumer receives the second.

## Checked
Method: docs-checked 2026-11-09 against the raw last-value-queues.adoc source (read in full); key configuration, legacy flag, deprecation note and clustering limit match.
