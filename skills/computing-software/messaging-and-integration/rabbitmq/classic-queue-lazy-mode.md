---
id: computing-software.messaging-and-integration.rabbitmq.classic-queue-lazy-mode
name: classic-queue-lazy-mode
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, classic-queue-lazy-mode]
level: advanced
status: docs-checked
description: "Understand lazy queues: in recent versions classic queues behave lazily by default, making the lazy mode setting effectively a no-op."
sources:
  - https://www.rabbitmq.com/docs/lazy-queues
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lazy queue mode

**Goal:** Avoid memory spikes from long classic queues.

## Steps
1. Until RabbitMQ 3.12, classic queues could be configured in `lazy` mode, which wrote all messages to disk and kept none in memory. RabbitMQ no longer supports lazy mode.
2. The setting is now ignored. Current classic queues write messages to disk with a short delay, keep a small subset in memory for fast delivery, and skip the disk write if a consumer acknowledges the message first.
3. There is no per-queue memory or latency trade-off to choose any more.

## Failure modes
- Setting lazy mode on a current version has no effect.

## Verify
- Compare node memory (`rabbitmq-diagnostics memory_breakdown`) before and after a million-message backlog.

## Checked

Date: 2026-11-02. Confirmed in the Lazy Queues page (docs/lazy-queues) and the rabbitmq-diagnostics man page (`memory_breakdown`). Removed as not stated there: the `x-queue-mode` argument name and the advice to prefer quorum queues or streams for backlogs.

Method: documentation only; no commands were run.
