---
id: computing-software.messaging-and-integration.apache-activemq-artemis.amqp-producer-flow-control
name: amqp-producer-flow-control
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,amqp,amqp-credits,max-size-bytes-reject-threshold,block,flow-control,activemq-artemis]
level: advanced
status: docs-checked
description: "Understand AMQP credit-based BLOCK: 100 message credits issued and refreshed at 30, and the max-size-bytes-reject-threshold hard limit that rejects messages."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/flow-control.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AMQP producer flow control

Core and AMQP implement address-full `BLOCK` differently. Core credits are bytes; AMQP credits are a count of messages regardless of size.

- The broker issues 100 credits to an AMQP client at a time and refreshes them when the client's credits reach 30.
- It stops issuing credits once the address is full (the `max-size-bytes` limit with `address-full-policy` set to `BLOCK`).
- Because credits are whole messages, a client can exceed the address bound significantly by spending its remaining credits on large messages.

## Hard limit
`max-size-bytes-reject-threshold` (address-setting, default `-1`, no limit) is an upper bound on address size in bytes. Once reached, the broker starts rejecting AMQP messages. It gives a soft limit (`max-size-bytes` with back pressure through credits) and a hard limit (the reject threshold) that protects the broker.

```xml
<address-setting match="orders">
   <max-size-bytes>10485760</max-size-bytes>
   <address-full-policy>BLOCK</address-full-policy>
   <max-size-bytes-reject-threshold>20971520</max-size-bytes-reject-threshold>
</address-setting>
```
(The size values are examples, in bytes.)

## Checked
2026-11-03. Confirmed against the Artemis user manual page flow-control, section Blocking AMQP Producers, and address-settings (max-size-bytes-reject-threshold). Removed: the Verify step.
Method: documentation only; no commands were run.
