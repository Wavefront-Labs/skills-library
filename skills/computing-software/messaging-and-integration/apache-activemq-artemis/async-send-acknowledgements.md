---
id: computing-software.messaging-and-integration.apache-activemq-artemis.async-send-acknowledgements
name: async-send-acknowledgements
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,sendacknowledgementhandler,confirmationwindowsize,asynchronous-send,send-acknowledgements,activemq-artemis]
level: sme
status: docs-checked
description: "Get non-blocking sends with guaranteed arrival by setting confirmationWindowSize and a SendAcknowledgementHandler on a Core ClientSession."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/send-guarantees.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Asynchronous send acknowledgements

**Goal:** have every message confirmed as received by the server without blocking each send on a network round trip, so throughput is bound by bandwidth rather than latency.

The Core client sends in one direction without blocking and receives acknowledgements asynchronously in a separate stream.

## Steps
1. Set `confirmationWindowSize` to a positive integer on the connection factory or client session factory, for example 10MiB. This is required.
2. Implement `org.apache.activemq.artemis.api.core.client.SendAcknowledgementHandler` and set an instance on your `ClientSession`.
3. Send as normal. As messages reach the server, your handler's `sendAcknowledged(ClientMessage message)` is later called with a reference to each message sent.

The window size is described under client failover in the manual.

## Why
The comparison with blocking sends: 4000 messages/s at 0.25 ms RTT versus a theoretical ~89478 messages/s on 1 Gb Ethernet (see `blocking-sends-and-acknowledgements`).

## Checked

Method: docs-checked 2026-11-09 against send-guarantees.adoc (read in full). Removed the Verify step and unsupported advice.
