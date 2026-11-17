---
id: computing-software.messaging-and-integration.rabbitmq.web-stomp
name: web-stomp
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, web-stomp]
level: practitioner
status: docs-checked
description: "Expose STOMP over WebSocket with rabbitmq_web_stomp for browser clients, behind TLS and with restricted users."
sources:
  - https://www.rabbitmq.com/docs/web-stomp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web STOMP

**Goal:** Let browsers talk to RabbitMQ without a gateway.

## Steps
1. `rabbitmq-plugins enable rabbitmq_web_stomp`; the WebSocket endpoint is `ws://host:15674/ws`.
2. For TLS (WSS) configure the `web_stomp.ssl` section; the guide's example uses port 15673, with certificate file, private key and CA bundle mandatory.
3. Create a separate user for production; the default `guest` user is only allowed from localhost.
4. Do not embed admin credentials in browser code.

## Failure modes
- Broad permissions on browser-facing users expose the broker.

## Verify
- Open a WebSocket from a test page; the connection appears in `rabbitmqctl list_connections`.

## Checked

Date: 2026-11-02. Confirmed on the Web STOMP guide. Fixed: the skill gave 15671 for TLS, which is the management TLS port; the guide's WSS example port is 15673. Removed: dedicated vhost advice.

Method: documentation only; no commands were run.
