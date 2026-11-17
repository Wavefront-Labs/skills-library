---
id: computing-software.messaging-and-integration.rabbitmq.dead-letter-exchange
name: dead-letter-exchange
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, dead-letter-exchange, rmq-dlx]
level: practitioner
status: docs-checked
description: "Configure a DLX by policy so rejected, expired or overflowed messages are routed to a parking queue."
sources:
  - https://www.rabbitmq.com/docs/dlx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dead letter exchange

**Goal:** Capture failed messages instead of losing them.

## Steps
1. Policy: `rabbitmqctl set_policy dlx "^work\." '{"dead-letter-exchange":"dlx","dead-letter-routing-key":"dead"}' --apply-to queues`.
2. Bind a durable queue to the DLX.
3. Inspect the x-death header for reason, count and original queue.
4. Alert on DLX queue depth.

## Failure modes
- A dead-letter cycle (the same message reaching the same queue twice) is detected and the message dropped if there was no rejection in the entire cycle.
- Quorum queues support at-least-once dead-lettering; classic queues do not.

## Verify
- Reject a message with requeue=false and find it in the DLX queue.

## Checked

Date: 2026-11-02. Confirmed in the Dead Letter Exchanges page (docs/dlx) and Classic Queues guide: policy keys `dead-letter-exchange` and `dead-letter-routing-key`, `x-death` header, cycle rule, at-least-once dead-lettering on quorum queues only. The `--apply-to queues` policy form matches the page's own example.

Method: documentation only; no commands were run.
