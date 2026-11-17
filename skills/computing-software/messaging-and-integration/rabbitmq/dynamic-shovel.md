---
id: computing-software.messaging-and-integration.rabbitmq.dynamic-shovel
name: dynamic-shovel
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, dynamic-shovel, rmq-shovel]
level: advanced
status: docs-checked
description: "Create runtime shovels with set_parameter to move messages between queues or exchanges, including across clusters."
sources:
  - https://www.rabbitmq.com/docs/shovel-dynamic
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic shovel

**Goal:** Move messages reliably between brokers.

## Steps
1. `rabbitmq-plugins enable rabbitmq_shovel rabbitmq_shovel_management`.
2. `rabbitmqctl set_parameter shovel s1 '{"src-protocol":"amqp091","src-uri":"amqp://","src-queue":"a","dest-protocol":"amqp091","dest-uri":"amqps://host","dest-queue":"b"}'`.
3. `ack-mode` defaults to `on-confirm`: acknowledge to the source after the destination confirms; it handles network and broker failures without loss and is the slowest.
4. Delete it when done: `rabbitmqctl clear_parameter shovel s1` (or use `src-delete-after`).

## Failure modes
- `ack-mode` `on-publish` and `no-ack` can lose messages on network or broker failures.

## Verify
- `rabbitmqctl shovel_status` shows the shovel running.

## Checked

Date: 2026-11-02. Confirmed on the Dynamic Shovels guide: parameter keys, ack-mode values and default, `clear_parameter`, `shovel_status`, `src-delete-after`. Removed: the unconfirmed "keeps moving traffic" failure mode.

Method: documentation only; no commands were run.
