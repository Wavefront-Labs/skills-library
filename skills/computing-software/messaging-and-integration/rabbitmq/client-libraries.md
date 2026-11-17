---
id: computing-software.messaging-and-integration.rabbitmq.client-libraries
name: client-libraries
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, client-libraries, rmq-clients]
level: practitioner
status: docs-checked
description: "Pick maintained client libraries (Java, .NET, Pika, amqplib) and apply their pooling and thread-safety rules."
sources:
  - https://www.rabbitmq.com/client-libraries/devtools
  - https://www.rabbitmq.com/docs/connections
  - https://www.rabbitmq.com/docs/channels
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client libraries

**Goal:** Use clients correctly.

## Steps
1. See the Client Libraries and Developer Tools page for the list of official clients (Java and .NET among them) and community libraries.
2. Keep connections long-lived and give each thread its own channel (or use a channel pool).
3. Set a connection name via the `connection_name` entry in the client properties for observability.

## Failure modes
- Sharing a channel between threads is discouraged by the channels guide.

## Verify
- `rabbitmqctl list_connections client_properties`.

## Checked

2026-11-02. Confirmed in client-libraries/devtools, docs/connections, docs/channels and the rabbitmqctl man page: official Java and .NET clients, connection_name, channel per thread, client_properties item. Removed: the named community libraries (Pika, amqplib, amqp091-go not found on the page) and the "protocol errors" claim.
Method: documentation only; no commands were run.
