---
id: computing-software.messaging-and-integration.rabbitmq.exchange-types
name: exchange-types
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, exchange-types, rmq-exchanges]
level: intro
status: docs-checked
description: "Choose among direct, fanout, topic and headers exchanges and declare them with the right durability and arguments."
sources:
  - https://www.rabbitmq.com/docs/exchanges
  - https://www.rabbitmq.com/tutorials/amqp-concepts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exchange types

**Goal:** Pick the exchange type that matches the routing need.

## Steps
1. direct: exact routing key match; fanout: ignore key, copy to all bound queues; topic: pattern match; headers: match header arguments.
2. Declare the exchange with your client's exchange.declare, giving name, type and durability.
3. Prefer durable exchanges for anything that must survive a restart.
4. A message that no binding routes is discarded (or sent to an alternate exchange) unless published as mandatory.

## Failure modes
- Redeclaring a queue with different attributes raises a 406 `PRECONDITION_FAILED` channel exception; the tutorial states this for queues.
- Using fanout where selective routing was intended duplicates traffic to every queue.

## Verify
- `rabbitmqctl list_exchanges name type durable` shows the type and flags.

## Checked

Date: 2026-11-02. Confirmed in the Exchanges guide (docs/exchanges), the AMQP 0-9-1 concepts tutorial and the rabbitmqctl man page (`list_exchanges`, `durable`). Removed as not stated there: the `rabbitmqadmin declare exchange` form and the redeclare-exchange error claim (the page states it for queues).

Method: documentation only; no commands were run.
