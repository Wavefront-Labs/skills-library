---
id: computing-software.messaging-and-integration.rabbitmq.message-ttl
name: message-ttl
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, message-ttl, rmq-ttl]
level: practitioner
status: docs-checked
description: "Expire messages with per-queue x-message-ttl or per-message expiration, knowing that per-message expiry is only checked at the queue head."
sources:
  - https://www.rabbitmq.com/docs/ttl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message TTL

**Goal:** Drop or dead-letter stale messages.

## Steps
1. Queue-level: policy `message-ttl` in milliseconds.
2. Per-message: the `expiration` property, which must be a string holding the number of milliseconds.
3. Expired messages are dead-lettered if a dead letter exchange is set. Quorum queues dead-letter them at the head of the queue; classic queues when they reach the head or on a policy change.
4. Queue-level TTL (the `message-ttl` policy) is the option to use when you need messages deleted to free resources.

## Failure modes
- With per-message TTL, expired messages can sit behind non-expired ones until those are consumed or expire; they keep using resources and show in queue statistics.
- When both queue and message TTL are set, the lower value applies.

## Verify
- Publish with expiration=1000, wait, and check `messages` drops to 0.

## Checked

Date: 2026-11-02. Confirmed in the TTL guide (docs/ttl): policy key `message-ttl`, string `expiration`, lower value wins, head-of-queue expiry, dead-lettering behaviour. Reworded: the stale-message failure mode, which the guide states for per-message TTL generally.

Method: documentation only; no commands were run.
