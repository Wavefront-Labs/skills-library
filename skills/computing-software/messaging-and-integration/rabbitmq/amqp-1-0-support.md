---
id: computing-software.messaging-and-integration.rabbitmq.amqp-1-0-support
name: amqp-1-0-support
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, amqp-1-0-support, rmq-amqp10]
level: practitioner
status: docs-checked
description: "Use AMQP 1.0 clients with RabbitMQ: native in 4.x, plugin in 3.x, with address v2 targets."
sources:
  - https://www.rabbitmq.com/docs/amqp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AMQP 1.0 support

**Goal:** Connect AMQP 1.0 clients.

## Steps
1. AMQP 1.0 is supported natively since RabbitMQ 4.0, on port 5672 alongside AMQP 0.9.1, with no plugin needed.
2. Use address format v2: `/exchanges/:exchange/:routing-key`, `/exchanges/:exchange`, `/queues/:queue`.
3. AMQP 1.0 connections must use SASL (username and password, a JWT, or an x.509 certificate via `EXTERNAL`); RabbitMQ rejects a connection that does not use SASL.

## Failure modes
- Addresses name exchanges and queues, and a queue named in a target or source address must already exist.

## Verify
- `rabbitmqctl list_amqp10_connections` lists the connection.

## Checked

Date: 2026-11-02. Confirmed in the AMQP 1.0 guide (docs/amqp) and the rabbitmqctl man page: native support since 4.0, port 5672, SASL requirement, authentication options, v2 addresses, `list_amqp10_connections`. Removed as not stated there: the 3.x plugin name and the `{1,0}` protocol value.

Method: documentation only; no commands were run.
