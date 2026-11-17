---
id: computing-software.messaging-and-integration.rabbitmq.connection-recovery
name: connection-recovery
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, connection-recovery]
level: practitioner
status: docs-checked
description: "Enable client automatic connection and topology recovery with backoff so apps survive broker restarts."
sources:
  - https://www.rabbitmq.com/docs/connections
  - https://www.rabbitmq.com/docs/heartbeats
  - https://www.rabbitmq.com/docs/confirms
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection recovery

**Goal:** Recover from drops without manual restarts.

## Steps
1. Use a client library with automatic connection recovery: the RabbitMQ Java and .NET clients support it. Other clients may leave recovery to the application, usually with documented examples of connection and topology recovery.
2. Recover topology (exchanges, queues, bindings, consumers) on reconnect.
3. Use heartbeats so dead peers are detected (see the heartbeats guide).

## Failure modes
- A message written to the socket may have been lost along the way; only publisher confirms tell you the broker took responsibility, so republish unconfirmed messages.

## Verify
- Restart a node and confirm consumers resume with `rabbitmqctl list_consumers`.

## Checked

2026-11-02. Confirmed in docs/connections: Java and .NET automatic recovery, other clients leave it to the application; docs/confirms: publishers cannot assume a written message arrived; rabbitmqctl man page: list_consumers. Removed: property name `automaticRecoveryEnabled`, Pika advice, jittered-backoff advice and exclusive/server-named queue claim (not in pages).
Method: documentation only; no commands were run.
