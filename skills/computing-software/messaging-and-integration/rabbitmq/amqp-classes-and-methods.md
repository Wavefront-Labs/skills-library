---
id: computing-software.messaging-and-integration.rabbitmq.amqp-classes-and-methods
name: amqp-classes-and-methods
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, amqp-classes-and-methods]
level: sme
status: docs-checked
description: "Know the main AMQP classes (connection, channel, exchange, queue, basic, confirm, tx) and key methods."
sources:
  - https://www.rabbitmq.com/resources/specs/amqp0-9-1.pdf
  - https://github.com/rabbitmq/amqp-0.9.1-spec/blob/main/xml/amqp0-9-1.extended.xml
  - https://www.rabbitmq.com/docs/extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AMQP classes and methods

**Goal:** Map client calls to protocol methods.

## Steps
1. Classes in the extended 0-9-1 spec: connection, channel, exchange, queue, basic, tx and confirm. Typical calls: connection.start, tune, open; channel.open; exchange.declare; queue.declare, queue.bind; basic.qos, consume, publish, ack; confirm.select.
2. RabbitMQ extensions to 0-9-1 include basic.nack (rejects multiple messages), publisher confirms, exchange-to-exchange bindings, consumer cancellation notifications, alternate exchanges, per-queue and per-message TTL, and dead letter exchanges.
3. Reply codes from the extended spec: 311 content-too-large, 312 no-route, 313 no-consumers (soft errors); 320 connection-forced (hard error); 403 access-refused, 404 not-found, 405 resource-locked, 406 precondition-failed (soft errors); 501 frame-error (hard error).

## Failure modes
- Treating extensions as portable to other AMQP brokers.

## Verify
- Trace one publish and name each frame.

## Checked
2026-11-09. Confirmed against the extended AMQP 0-9-1 XML spec (class names, method names, constant names, values and soft or hard class) and the RabbitMQ AMQP 0-9-1 Protocol Extensions page (nack, confirms, consumer cancellation, exchange-to-exchange bindings, alternate exchanges, TTL, dead letter exchanges). Added the error class of each code; removed the version note.
Method: documentation only; no commands were run.
