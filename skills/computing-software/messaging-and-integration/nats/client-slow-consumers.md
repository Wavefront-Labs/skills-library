---
id: computing-software.messaging-and-integration.nats.client-slow-consumers
name: client-slow-consumers
category: computing-software
field: messaging-and-integration
product: nats
tags: [slow-consumer, pending-limits, subscription, backpressure, client-buffer]
level: practitioner
status: docs-checked
description: "Handle slow consumers in clients: pending message/byte limits per subscription, drop behavior, and throttle/queue/persist patterns."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/using-nats/developing-with-nats/events/slow.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep a subscriber from being cut off by the server when it cannot keep up.

The server drops connections whose clients are too slow. To absorb bursts, many client libraries buffer incoming messages per subscription. When that buffer is full, the library drops messages (and typically raises an async error) instead of letting the connection stall; that keeps the connection healthy but means the application must cope with loss.

Patterns the docs list:
- request-reply to throttle senders,
- queue subscriptions so several subscribers split the work,
- persist messages (JetStream) so slow consumers can catch up.

Limits are usually two controls on the pending queue: a message count and a byte size. Go example: `sub1.SetPendingLimits(1000, 5*1024*1024)` limits to 1,000 messages or 5 MB, whichever comes first.

Gotchas: disabling limits (setting them to 0) can help find problems but is dangerous in production, because an unbounded buffer can exhaust memory. The cache is usually per subscriber but this varies by library; defaults and the ability to disable them are library specific. Limits are useful when the problem is bursty publishers, not a continuous performance mismatch.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
