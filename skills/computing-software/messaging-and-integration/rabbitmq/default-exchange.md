---
id: computing-software.messaging-and-integration.rabbitmq.default-exchange
name: default-exchange
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, default-exchange]
level: intro
status: docs-checked
description: "Use the nameless default direct exchange that routes by queue name, and know its limits (no explicit bindings, cannot be deleted)."
sources:
  - https://www.rabbitmq.com/tutorials/amqp-concepts
  - https://www.rabbitmq.com/docs/publishers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default exchange

**Goal:** Send a simple message straight to a named queue.

## Steps
1. Publish with exchange "" and routing key equal to the queue name.
2. The default exchange is a nameless direct exchange; every queue is automatically bound to it with the queue name as binding key. RabbitMQ does not allow bind or unbind operations on it; trying gives an error.
3. Prefer a named exchange when routing may grow later.

## Failure modes
- A message that cannot be routed (a typo in the routing key) is discarded unless it is published with the `mandatory` property, in which case it is returned to the publisher.
- Applications that rely on it cannot later fan out without code changes.

## Verify
- Publish to key "q1" and check `rabbitmqctl list_queues name messages` for q1.

## Checked

Date: 2026-11-02. Confirmed in the AMQP 0-9-1 concepts tutorial (default exchange section) and the Publishers guide (unroutable and mandatory behaviour).

Method: documentation only; no commands were run.
