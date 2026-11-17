---
id: computing-software.messaging-and-integration.rabbitmq.queue-ttl
name: queue-ttl
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, queue-ttl]
level: practitioner
status: docs-checked
description: "Auto-delete unused queues after a period with x-expires, useful for temporary reply or per-session queues."
sources:
  - https://www.rabbitmq.com/docs/ttl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue TTL (x-expires)

**Goal:** Clean up abandoned queues.

## Steps
1. Set the `expires` policy or the `x-expires` queue argument, in milliseconds; it must be a positive integer.
2. A queue expires only when it is unused: no consumers, not recently redeclared (redeclaring renews the lease) and no `basic.get` for the expiration period.
3. Queue expiration generally only makes sense for transient (non-durable) classic queues; streams do not support it.

## Failure modes
- A very short period can delete a queue while its clients are reconnecting, since it counts as unused.

## Verify
- Declare with x-expires=5000, leave idle, and confirm it disappears from `rabbitmqctl list_queues`.

## Checked

Date: 2026-11-02. Confirmed in the TTL guide (docs/ttl), queue TTL section. Removed as not stated there: the claim that a queue is deleted even with messages.

Method: documentation only; no commands were run.
