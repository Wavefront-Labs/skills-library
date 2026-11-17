---
id: computing-software.messaging-and-integration.rabbitmq.amqp-1-0-addressing
name: amqp-1-0-addressing
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, amqp-1-0-addressing]
level: advanced
status: docs-checked
description: "Address exchanges and queues from AMQP 1.0 clients and understand credit-based flow and settlement modes."
sources:
  - https://www.rabbitmq.com/docs/amqp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AMQP 1.0 addressing

**Goal:** Use AMQP 1.0 links correctly.

## Steps
1. Sender target addresses (format v2): `/exchanges/:exchange/:routing-key`, `/exchanges/:exchange` or `/queues/:queue`; or the null address with each message's `to` field set to one of those strings. A receiver's source address is `/queues/:queue` (the queue must exist). Percent-encode names, so a `/` in a routing key becomes `%2F`.
2. To use another virtual host, prefix the `hostname` field of the open frame with `vhost:`, for example `vhost:tenant-1`.
3. Address format v1 (`/exchange/...`, `/queue/...`, `/topic/...`) is deprecated in 4.0; use v2.

## Failure modes
- A message that cannot be routed (for example no queue bound) is settled with the `released` outcome.
- The default exchange `""` is not allowed in the `/exchanges/` formats; use `/queues/:queue` instead.

## Verify
- Send to a bound exchange and see the `accepted` outcome; send with no binding and see `released`.

## Checked

Date: 2026-11-02. Confirmed in the RabbitMQ AMQP 1.0 guide (docs/amqp): v2 target and source formats, null target with `to`, percent-encoding, `vhost:` hostname prefix, v1 deprecation, `released` for unroutable messages, `accepted` outcome. Removed as not stated there: settle-mode advice, link-credit statement, presettled message-loss note.

Method: documentation only; no commands were run.
