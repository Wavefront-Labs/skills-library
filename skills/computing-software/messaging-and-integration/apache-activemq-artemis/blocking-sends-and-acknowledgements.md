---
id: computing-software.messaging-and-integration.apache-activemq-artemis.blocking-sends-and-acknowledgements
name: blocking-sends-and-acknowledgements
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,blockondurablesend,blockonnondurablesend,blockonacknowledge,at-most-once,send-guarantees,activemq-artemis]
level: advanced
status: docs-checked
description: "Make Core sends and acks wait for server confirmation with blockOnDurableSend (default true), blockOnNonDurableSend and BlockOnAcknowledge, and know the RTT cost."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/send-guarantees.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blocking sends and acknowledgements

For non-transacted Core sessions you can make `send` and `acknowledge` wait for the server's response via URL parameters:
- `blockOnDurableSend` (default `true`): sends of durable messages block until they reach the server and a response returns.
- `blockOnNonDurableSend` (default `false`): same for non-durable messages.
- `BlockOnAcknowledge` (default `false`): acknowledge blocks until the server confirms it; set `true` for a strict at-most-once delivery policy.

```
tcp://localhost:61616?blockOnDurableSend=true&blockOnNonDurableSend=false
```

## Cost
Each blocking send needs a network round trip, so send rate is bounded by RTT rather than bandwidth. The manual's arithmetic: with a 0.25 ms RTT at most 1000/0.25 = 4000 blocking sends per second, against a theoretical 89478 messages per second on 1 Gb Ethernet (1500-byte messages, 1500 MTU) when sends do not block. To keep reliability and speed, batch sends in a transaction (only commit and rollback block) or use asynchronous send acknowledgements (see `async-send-acknowledgements`).

## Checked

Method: docs-checked 2026-11-09 against send-guarantees.adoc (read in full). Removed the Verify step and unsupported advice.
