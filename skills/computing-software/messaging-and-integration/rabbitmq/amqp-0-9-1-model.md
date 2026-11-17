---
id: computing-software.messaging-and-integration.rabbitmq.amqp-0-9-1-model
name: amqp-0-9-1-model
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, amqp-0-9-1-model, rmq-amqp-model]
level: intro
status: docs-checked
description: "Explain the AMQP 0-9-1 model: publishers send to exchanges, bindings route to queues, consumers read queues; the broker does the routing."
sources:
  - https://www.rabbitmq.com/tutorials/amqp-concepts
  - https://www.rabbitmq.com/docs/ae
  - https://www.rabbitmq.com/docs/confirms
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AMQP 0-9-1 model

**Goal:** Reason about message flow before configuring anything.

## Steps
1. Publishers send to an exchange; the default exchange is a direct exchange with no name that routes by queue name (every queue is bound to it with its name as the key).
2. Exchanges apply bindings and route messages to queues.
3. The broker either delivers messages to consumers subscribed to a queue, or consumers fetch (pull) messages from queues on demand.
4. Messages carry a routing key, properties and a body.

## Failure modes
- A message that cannot be routed may be returned to the publisher (when published as mandatory), dropped, or sent to an alternate exchange or dead letter queue.
- Publishing is not delivery: use publisher confirms for assurance.

## Verify
- Declare an exchange and queue, bind them, publish, then run `rabbitmqctl list_bindings` and `rabbitmqctl list_queues name messages`.

## Checked

2026-11-02. Confirmed in tutorials/amqp-concepts, docs/ae, docs/confirms: default exchange, binding, unroutable message handling (return, drop, alternate exchange, dead letter), mandatory flag, confirms; rabbitmqctl man page: list_bindings, list_queues messages. Removed: the property list and "avoid basic.get for throughput" (not in pages read).
Method: documentation only; no commands were run.
