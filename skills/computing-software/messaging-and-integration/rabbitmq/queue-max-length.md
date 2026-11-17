---
id: computing-software.messaging-and-integration.rabbitmq.queue-max-length
name: queue-max-length
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, queue-max-length]
level: practitioner
status: docs-checked
description: "Bound queues with max-length and max-length-bytes and pick an overflow behaviour (drop-head, reject-publish)."
sources:
  - https://www.rabbitmq.com/docs/maxlength
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue length limits

**Goal:** Protect memory and disk from runaway queues.

## Steps
1. Policy: `rabbitmqctl set_policy ml ".*" '{"max-length":100000,"overflow":"reject-publish"}' --apply-to queues`.
2. By default, when the limit is reached the oldest messages are dropped or dead-lettered from the front. With `overflow` set to `reject-publish` the newest messages are discarded and, if publisher confirms are on, the publisher gets `basic.nack`; `reject-publish-dlx` also dead-letters the rejected messages.
3. Only ready messages count; messages unacknowledged by consumers do not. If a policy and an argument both set a limit, the minimum is used.

## Failure modes
- With `reject-publish` and no publisher confirms, the publisher is not told its message was discarded.

## Verify
- Fill past the limit and observe drops or nacks.

## Checked

Date: 2026-11-02. Confirmed in the Queue Length Limit page (docs/maxlength): `max-length` and `overflow` policy keys, default behaviour, nack with confirms, ready-only counting, minimum of policy and argument. Removed: the name `drop-head`, which the page does not use.

Method: documentation only; no commands were run.
