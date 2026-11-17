---
id: computing-software.messaging-and-integration.rabbitmq.classic-queues
name: classic-queues
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, classic-queues, rmq-classic-queues]
level: practitioner
status: docs-checked
description: "Know how classic queues behave: single-node, non-replicated in 4.x, best for transient or exclusive workloads, with the v2 storage implementation."
sources:
  - https://www.rabbitmq.com/docs/classic-queues
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Classic queues

**Goal:** Decide when a classic queue is still the right type.

## Steps
1. Classic queues are the original, non-replicated FIFO queue type; they are the default unless the virtual host overrides the default queue type. Classic queues version 1 support was removed in RabbitMQ 4.0, so version 2 is the implementation.
2. Use where data safety is not a priority. Classic queues support exclusivity, TTL, length limits, message and consumer priority and dead letter exchanges (but not at-least-once dead-lettering or poison message handling). For data safety use quorum queues or streams.
3. Classic queue mirroring was removed in RabbitMQ 4.x; classic queues are not replicated. Use quorum queues for replication.
4. Declare with `x-queue-type` set to `classic` (the default when none is given and the virtual host default is unchanged).

## Failure modes
- Relying on mirroring on 4.x: policies for ha-mode no longer apply.
- Classic queue data is not replicated, so losing a node loses access to that data.

## Verify
- `rabbitmqctl list_queues name type` shows `classic`.

## Checked

Date: 2026-11-02. Confirmed in the Classic Queues guide (docs/classic-queues), Queues guide (docs/queues) and Policies guide (docs/policies, mirroring removed in 4.x). Removed as not stated there: the per-queue store description and the temporary/high-churn use case.

Method: documentation only; no commands were run.
