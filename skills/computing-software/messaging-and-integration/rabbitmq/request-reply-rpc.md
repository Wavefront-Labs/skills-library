---
id: computing-software.messaging-and-integration.rabbitmq.request-reply-rpc
name: request-reply-rpc
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, request-reply-rpc, rmq-rpc]
level: practitioner
status: docs-checked
description: "Implement request-reply using reply_to, correlation_id and a reply queue, or direct reply-to."
sources:
  - https://www.rabbitmq.com/docs/direct-reply-to
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Request-reply RPC

**Goal:** Synchronous calls over messaging.

## Steps
1. The requester sets `reply_to` and `correlation_id` and applies its own timeout.
2. For direct reply-to, consume from the pseudo-queue `amq.rabbitmq.reply-to` in no-ack mode; there is no need to declare it first.
3. The server publishes the reply to the `reply_to` address and copies the `correlation_id`.

## Failure modes
- `amq.rabbitmq.reply-to` is not a real queue: it cannot be deleted and does not appear in the management plugin or `rabbitmqctl list_queues`.
- Without a timeout, callers hang if the reply is lost.

## Verify
- A round trip returns a matching `correlation_id`.

## Checked

2026-11-02. Confirmed in docs/direct-reply-to: pseudo-queue name, no-ack consume, no declaration needed, not listed in list_queues. Removed: the claim that the server replies via the default exchange (the guide describes replying to the reply_to address) and the post-restart reply-loss claim.
Method: documentation only; no commands were run.
