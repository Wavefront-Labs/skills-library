---
id: computing-software.messaging-and-integration.rabbitmq.queue-declare-arguments
name: queue-declare-arguments
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, queue-declare-arguments]
level: practitioner
status: docs-checked
description: "Set optional queue arguments such as x-queue-type, x-message-ttl, x-max-length and x-dead-letter-exchange, preferring policies for runtime changes."
sources:
  - https://www.rabbitmq.com/docs/queues
  - https://www.rabbitmq.com/docs/ttl
  - https://www.rabbitmq.com/docs/maxlength
  - https://www.rabbitmq.com/docs/dlx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue declare arguments

**Goal:** Configure queue behaviour without breaking redeclarations.

## Steps
1. Arguments are set at declare time: x-queue-type, x-message-ttl, x-expires, x-max-length, x-max-length-bytes, x-overflow, x-dead-letter-exchange, x-dead-letter-routing-key.
2. Prefer policies for keys that can be set by policy; they are more flexible and need no application redeployment.
3. Queue type and `x-max-priority` must be set at declaration and cannot be changed afterwards.

## Failure modes
- Redeclaring with different attributes raises a channel error 406 (`PRECONDITION_FAILED`).

## Verify
- `rabbitmqctl list_queues name arguments policy`.

## Checked

Date: 2026-11-02. Confirmed on the Queues, TTL, Queue Length Limits and Dead Letter Exchanges guides: every argument name, 406 behaviour, fixed-at-declare properties. Removed: the "create a new queue and migrate" advice.

Method: documentation only; no commands were run.
