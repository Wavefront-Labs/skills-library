---
id: computing-software.messaging-and-integration.rabbitmq.connection-blocked
name: connection-blocked
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, connection-blocked]
level: practitioner
status: docs-checked
description: "Handle connection.blocked and unblocked notifications when alarms stop publishers."
sources:
  - https://www.rabbitmq.com/docs/connection-blocked
  - https://www.rabbitmq.com/docs/connections
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blocked connections

**Goal:** Make publishers resilient to alarms.

## Steps
1. Register blocked/unblocked callbacks in the client; the broker sends `connection.blocked` and `connection.unblocked` to clients that support the capability.
2. Stop publishing while blocked and resume on unblock. `connection.unblocked` is sent only when all alarms are cleared.
3. Use separate connections for publishers and consumers.

## Failure modes
- Sharing one connection between publishers and consumers means flow control or a blocked connection also hits the consumers.

## Verify
- Trigger an alarm in test and see the blocked callbacks fire.

## Checked

Date: 2026-11-02. Confirmed in the Blocked Connection Notifications page (docs/connection-blocked) and the Connections guide (docs/connections, separate publisher and consumer connections). Removed as not stated there: the buffering advice and the deadlock claim.

Method: documentation only; no commands were run.
