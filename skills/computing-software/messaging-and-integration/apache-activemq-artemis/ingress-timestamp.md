---
id: computing-software.messaging-and-integration.apache-activemq-artemis.ingress-timestamp
name: ingress-timestamp
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,enable-ingress-timestamp,ingress-time,amq-ingress-timestamp,x-opt-ingress-time,activemq-artemis]
level: practitioner
status: docs-checked
description: "Stamp messages with the broker's receive time via enable-ingress-timestamp and read it as x-opt-ingress-time, _AMQ_INGRESS_TIMESTAMP or ingress-timestamp."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/address-settings.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ingress timestamp

**Goal:** have the broker record when it received each message, independent of producer clocks.

Set `enable-ingress-timestamp` to `true` (default `false`) in an address-setting. The value is milliseconds since the epoch, and where it is stored depends on protocol:
- AMQP: a `long` message annotation named `x-opt-ingress-time`.
- Core messages (used by the Core and OpenWire protocols): a long property named `_AMQ_INGRESS_TIMESTAMP`.
- STOMP: a frame header named `ingress-timestamp`.

```xml
<address-setting match="audit.#">
   <enable-ingress-timestamp>true</enable-ingress-timestamp>
</address-setting>
```
Use it to measure end-to-end latency or queue dwell time using one clock (the broker's) instead of comparing producer and consumer clocks.

## Verify
Send a message to a matching address and inspect the property or annotation on the consumed message.

## Notes
The stamp is the broker's own time, so the difference between it and the consumer's receive time covers broker residence plus delivery. The setting applies per address match, so enable it only on the address ranges you need. The AMQP annotation is a long, so read it as an epoch-millisecond number.

## Checked

Method: docs-checked 2026-11-09 against address-settings.adoc (raw, enable-ingress-timestamp entry)
