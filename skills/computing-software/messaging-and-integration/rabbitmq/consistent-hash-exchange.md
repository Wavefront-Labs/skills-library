---
id: computing-software.messaging-and-integration.rabbitmq.consistent-hash-exchange
name: consistent-hash-exchange
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, consistent-hash-exchange]
level: advanced
status: docs-checked
description: "Shard messages across queues with the consistent hash exchange plugin keyed by routing key or header."
sources:
  - https://github.com/rabbitmq/rabbitmq-server/blob/main/deps/rabbitmq_consistent_hash_exchange/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consistent hash exchange

**Goal:** Partition work while keeping per-key order.

## Steps
1. `rabbitmq-plugins enable rabbitmq_consistent_hash_exchange`; exchange type `x-consistent-hash`.
2. The binding key is a number given as a string; it is the binding weight (a queue bound with twice the weight gets about twice the routing keys).
3. The hash is computed from the routing key by default; declare the exchange with the `hash-header` argument to hash on a named header instead (messages lacking the header all go to one queue).

## Failure modes
- Adding or removing bindings changes the ring, so a given routing key may route to a different queue.

## Verify
- Publish keys and see stable queue assignment.

## Checked

Date: 2026-11-02. Confirmed in the plugin README (rabbitmq_consistent_hash_exchange): plugin name, `x-consistent-hash` type, string weights, `hash-header`, rebalancing on binding changes. The README states all messages with the same routing key go to the same queue, which the goal line relies on.

Method: documentation only; no commands were run.
