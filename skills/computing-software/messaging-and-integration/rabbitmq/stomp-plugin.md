---
id: computing-software.messaging-and-integration.rabbitmq.stomp-plugin
name: stomp-plugin
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, stomp-plugin, rmq-stomp]
level: practitioner
status: docs-checked
description: "Enable STOMP and use destinations like /queue, /exchange and /topic to reach AMQP entities."
sources:
  - https://www.rabbitmq.com/docs/stomp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STOMP plugin

**Goal:** Serve STOMP clients and web sockets.

## Steps
1. `rabbitmq-plugins enable rabbitmq_stomp`; ports 61613 plain and 61614 TLS.
2. Destinations: `/exchange/<name>[/<key>]`, `/queue/<name>`, `/topic/<name>`, `/amq/queue/<name>`, plus `/temp-queue/` in reply-to headers.
3. `/queue/<name>` queues are created by the gateway, durable and non-exclusive by default; `/amq/queue` is for queues created outside the gateway.
4. For browsers enable `rabbitmq_web_stomp`.
5. Manual acknowledgements: subscribe with `ack:client` (or `client-individual`).

## Failure modes
- `SUBSCRIBE` or `SEND` to `/queue/<name>` creates that queue if missing.

## Verify
- Send a frame and see the queue in `rabbitmqctl list_queues`.

## Checked

Date: 2026-11-02. Confirmed on the STOMP guide: ports, destination types and queue defaults, ack modes. Removed: the "implicit queue prefixes" claim as worded.

Method: documentation only; no commands were run.
