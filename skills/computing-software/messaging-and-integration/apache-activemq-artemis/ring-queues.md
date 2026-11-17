---
id: computing-software.messaging-and-integration.apache-activemq-artemis.ring-queues
name: ring-queues
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,ring-queue,ring-size,default-ring-size,fixed-size-queue,consumerwindowsize,activemq-artemis]
level: advanced
status: docs-checked
description: "Bound a queue to a fixed size with ring-size or default-ring-size, evicting from the head, and know when in-delivery, scheduled or paged messages exceed it."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/ring-queues.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ring queues

**Goal:** a FIFO queue of fixed size: when a new message arrives at the tail and the count has reached the size, the message at the head is removed. With ring-size 3 and sends A, B, C, D the queue ends as B, C, D.

## Configure
```xml
<address name="myRing">
   <anycast>
      <queue name="myRing" ring-size="3" />
   </anycast>
</address>
```
Or set `default-ring-size` in an `address-setting` for matching addresses whose queues have no explicit `ring-size` (useful for auto-created queues; default `-1`, no limit):
```xml
<address-setting match="ring.#">
   <default-ring-size>3</default-ring-size>
</address-setting>
```
`ring-size` can be changed at runtime. Lowering it does not delete messages immediately; new arrivals stop the queue growing but it shrinks only through natural consumption.

## Why the size can look exceeded
- **In delivery:** messages sent to a consumer but unacknowledged cannot be removed. With ring-size 3 and one consumer, `messageCount` can reach 4 with `deliveringCount` 4. If the consumer closes without acking, the messages return to the head in reverse order and the oldest is dropped. Rollbacks behave the same. Reduce `consumerWindowSize` (default 1024 * 1024 bytes) to minimize messages in delivery.
- **Scheduled messages:** held in an intermediate buffer, counted in `messageCount`, but only placed at the head at their time (then possibly evicted).
- **Paging:** paged messages count in `messageCount` but are paged at address level. Avoid paging on addresses with ring queues: make the address fit in memory or use the `DROP`, `BLOCK` or `FAIL` `address-full-policy`.

## Checked
2026-11-03. Confirmed against the Artemis user manual page ring-queues: ring-size and default-ring-size, runtime update, in-delivery, scheduled and paging cases. Removed: the Verify step.
Method: documentation only; no commands were run.
