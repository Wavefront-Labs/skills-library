---
id: computing-software.messaging-and-integration.rabbitmq.dead-letter-reasons
name: dead-letter-reasons
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, dead-letter-reasons]
level: practitioner
status: docs-checked
description: "Know the four dead-letter reasons (rejected, expired, maxlen, delivery-limit) and read them from x-death."
sources:
  - https://www.rabbitmq.com/docs/dlx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dead letter reasons

**Goal:** Diagnose why a message was dead-lettered.

## Steps
1. Reasons: `rejected` (negatively acknowledged without requeue), `expired` (message TTL), `maxlen` (queue length limit exceeded), `delivery_limit` (quorum queue delivery-limit exceeded).
2. The `x-death` header is an array of entries; `x-first-death-queue`, `x-first-death-reason` and `x-first-death-exchange` record the first death.
3. Inspect the headers in the consumer of the dead-letter queue to branch on reason.

## Failure modes
- Entries accumulate in `x-death` when a message dies repeatedly.

## Verify
- Trigger each reason on a test queue and read x-death.

## Checked

Date: 2026-11-02. Confirmed in the Dead Letter Exchanges page (docs/dlx): the four reasons and the `x-first-death-*` headers. Removed as not stated there: the exact field list of an `x-death` entry, the headers-exchange routing idea and the drop-head remark.

Method: documentation only; no commands were run.
