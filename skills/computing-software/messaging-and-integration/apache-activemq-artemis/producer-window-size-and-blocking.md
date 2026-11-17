---
id: computing-software.messaging-and-integration.apache-activemq-artemis.producer-window-size-and-blocking
name: producer-window-size-and-blocking
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,producerwindowsize,blocking-producers,producer-flow-control,credits,max-size-bytes,activemq-artemis]
level: advanced
status: docs-checked
description: "Understand Core producer credits (producerWindowSize) and blocking producers with max-size-bytes plus BLOCK, including how credits can overshoot the limit."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/flow-control.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Producer window size and blocking producers

**Goal:** stop producers overwhelming the broker without paging.

Core producers may send only while they have credits; a message costs its size in bytes. When credits run low they request more. The amount requested at once is the window size, set by the `producerWindowSize` URI parameter; it caps bytes in flight on the connection.

## Blocking
Give the address a maximum size and the `BLOCK` policy:
```xml
<address-settings>
   <address-setting match="exampleQueue">
      <max-size-bytes>100000</max-size-bytes>
      <address-full-policy>BLOCK</address-full-policy>
   </address-setting>
</address-settings>
```
The server never issues more credits than the address limit allows, so when the address fills, producers block client-side until consumers free space. The limit covers all queues on the address; for a JMS topic it is the total of all subscriptions. The policy must be `BLOCK` for this to work.

## Overshoot and trust
Credits are allocated by the broker but checked only on the client. With several producers the broker can over-allocate: the address can exceed its limit by about (producers on the address) * (producer window size). A misbehaving client can ignore credits entirely.

## Default
In the default configuration all addresses block producers after 10 MiB of message data, so raise `max-size-bytes` or change the policy if you do not want that.

## Checked
2026-11-03. Confirmed against the Artemis user manual page flow-control, Producer flow control sections: credits, producerWindowSize, blocking example, overshoot formula, client-side credit checking and the 10 MiB default. Removed: the Verify step.
Method: documentation only; no commands were run.
