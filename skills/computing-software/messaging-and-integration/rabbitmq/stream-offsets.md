---
id: computing-software.messaging-and-integration.rabbitmq.stream-offsets
name: stream-offsets
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, stream-offsets]
level: practitioner
status: docs-checked
description: "Select where a stream consumer starts (first, last, next, offset, timestamp) with x-stream-offset and track offsets for resume."
sources:
  - https://www.rabbitmq.com/docs/streams
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stream consumer offsets

**Goal:** Replay or resume a stream deterministically.

## Steps
1. AMQP 0-9-1: set the consumer argument `x-stream-offset` to `first`, `last` (the last written chunk), `next`, a numeric offset, or a timestamp (POSIX seconds, based on message arrival time).
2. If unspecified, the consumer starts at `next`, the next offset written after it starts.
3. A numeric offset or timestamp out of range clamps to the start or end of the log.
4. Broker-provided offset tracking persists consumer offsets in the stream itself.

## Failure modes
- Starting at `first` on a very large stream makes the consumer read the whole retained log.

## Verify
- Consume with offset `first` and confirm the first delivery is the oldest retained message.

## Checked

Date: 2026-11-02. Confirmed on the Streams guide (Consuming, offset tracking). Removed: "default start position varies by client".

Method: documentation only; no commands were run.
