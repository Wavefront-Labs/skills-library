---
id: computing-software.messaging-and-integration.rabbitmq.idempotent-receiver
name: idempotent-receiver
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, idempotent-receiver, rmq-eip-reliability]
level: advanced
status: docs-checked
description: "Make consumers safe under redelivery by recording processed message ids."
sources:
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://www.rabbitmq.com/docs/confirms
  - https://www.rabbitmq.com/docs/publishers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Idempotent receiver

**Goal:** Tolerate duplicates.

## Steps
1. Have publishers set the `message_id` property on every message (RabbitMQ treats it as an arbitrary application value).
2. Store processed ids together with the side effect in one transaction, then ack. A redelivery has the `redeliver` property set to true, but a message may also be republished by the producer after a lost confirm, so check the store for every message, not only redeliveries.
3. Expire stored ids once duplicates can no longer arrive; choose the window from your retry and republish behaviour.

## Failure modes
- A dedupe store outside the transaction can still duplicate.
- A consumer can receive a message previously delivered to another consumer.

## Verify
- Redeliver a message and see one effect.

## Checked
2026-11-09. Confirmed on the RabbitMQ Acknowledgements page: unacked deliveries are requeued on channel or connection close, consumers must be written with idempotence in mind, `redeliver` is true on redeliveries, and a consumer can receive a message previously delivered to another consumer. Confirmed on the Publishers page: message id is an arbitrary message property. Idempotent Receiver is named on the EIP messaging index. Removed: the version note.
Method: documentation only; no commands were run.
