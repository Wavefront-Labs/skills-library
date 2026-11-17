---
id: computing-software.messaging-and-integration.rabbitmq.queue-properties
name: queue-properties
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, queue-properties, rmq-queues]
level: intro
status: docs-checked
description: "Declare queues with the right durability, exclusivity and auto-delete flags and know what each means for survival after restart."
sources:
  - https://www.rabbitmq.com/docs/queues
  - https://www.rabbitmq.com/docs/classic-queues
  - https://www.rabbitmq.com/docs/man/rabbitmqctl.8
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue properties

**Goal:** Declare queues that match the lifetime of the workload.

## Steps
1. Durable: the queue survives a broker restart.
2. Exclusive: used by only one connection and deleted when that connection closes. Auto-delete: a queue that has had at least one consumer is deleted when its last consumer unsubscribes.
3. Server-named queues: pass an empty string as the queue name and use the generated name the broker returns.
4. Queue durability is separate from message persistence; see "Queue Durability and how it relates to message persistence" in the queues guide.

## Failure modes
- Transient classic queues are discouraged, and support for them is deprecated and slated for removal in RabbitMQ 4.0 per the classic queues guide.

## Verify
- `rabbitmqctl list_queues name durable exclusive auto_delete type`.

## Checked

2026-11-02. Confirmed in docs/queues: durable, exclusive, auto-delete definitions, server-named queues; docs/classic-queues: transient queue deprecation (4.0); rabbitmqctl man page: list_queues info items name, durable, exclusive, auto_delete, type. Fixed: the skill said "exact version unconfirmed"; the guide gives 4.0. Removed: the "durable queue plus transient messages loses messages" line (the persistence detail is not in the pages I read).
Method: documentation only; no commands were run.
