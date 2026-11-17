---
id: computing-software.messaging-and-integration.rabbitmq.stream-basics
name: stream-basics
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, stream-basics, rmq-streams]
level: practitioner
status: docs-checked
description: "Use RabbitMQ streams, an append-only replicated log with non-destructive consumption, via the stream protocol or AMQP 0-9-1."
sources:
  - https://www.rabbitmq.com/docs/streams
  - https://www.rabbitmq.com/docs/stream
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stream basics

**Goal:** Choose streams for fan-out replay and very large backlogs.

## Steps
1. Declare with `x-queue-type=stream` (streams are always durable); use AMQP 0-9-1 or the dedicated stream protocol (default port 5552).
2. Enable the stream protocol plugin: `rabbitmq-plugins enable rabbitmq_stream`.
3. Consumers read without removing messages, so several consumers can read the same data from any point in the log.
4. AMQP 0-9-1 consumers need QoS prefetch and manual acknowledgements; the acknowledgement acts as a credit to advance the offset. Use per-consumer prefetch, not global.

## Failure modes
- A channel with global QoS enabled gets a channel error when consuming from a stream.
- Streams lack non-durable and exclusive modes, per-message TTL, message priority, consumer priority and dead letter exchanges.

## Verify
- `rabbitmqctl list_queues name type` (the `type` column shows the queue type).

## Checked

Date: 2026-11-02. Confirmed on the Streams guide and the Stream plugin page: declaration, port 5552, plugin, prefetch and global QoS error, feature matrix. Removed: "forgetting basic.qos gives an error" (the guide says consumption requires prefetch, and gives the error only for global QoS).

Method: documentation only; no commands were run.
