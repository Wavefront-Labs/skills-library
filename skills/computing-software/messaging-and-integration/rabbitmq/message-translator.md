---
id: computing-software.messaging-and-integration.rabbitmq.message-translator
name: message-translator
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, message-translator, rmq-eip-transformation]
level: practitioner
status: docs-checked
description: "Convert message formats between systems in a consumer-producer pair, setting content_type."
sources:
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://www.rabbitmq.com/docs/publishers
  - https://www.rabbitmq.com/docs/confirms
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message translator

**Goal:** Bridge formats.

## Steps
1. Consume from the source queue with manual acknowledgements, transform, publish to the target exchange with the right `content_type` and `content_encoding` message properties, and ack the source message only after the publish is confirmed (publisher confirms).
2. Copy `correlation_id` and `message_id` and application headers across.
3. Keep the transformer stateless; because unacked deliveries are redelivered after a failure, make it safe to run twice on the same message.

## Failure modes
- Dropping headers loses tracing.
- Acking before the confirm loses the message if the publish fails.

## Verify
- Compare input and output schemas.

## Checked
2026-11-09. Translator named on the EIP messaging index. The Publishers page lists `content_type`, `content_encoding`, `correlation_id` and `message_id` among standard message properties; content type and encoding are used by applications, not core RabbitMQ. The Acknowledgements page confirms manual acks, publisher confirms and redelivery on failure. Removed: the version note.
Method: documentation only; no commands were run.
