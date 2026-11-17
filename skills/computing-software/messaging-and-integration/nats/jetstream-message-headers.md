---
id: computing-software.messaging-and-integration.nats.jetstream-message-headers
name: jetstream-message-headers
category: computing-software
field: messaging-and-integration
product: nats
tags: [headers, nats-msg-id, deduplication, optimistic-concurrency, rollup, message-ttl]
level: practitioner
status: docs-checked
description: "Use JetStream publish headers: Nats-Msg-Id dedup, Nats-Expected-* concurrency checks, Nats-Rollup, Nats-TTL, and republish headers."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/nats-concepts/jetstream/headers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: apply the server-recognised headers on publish and understand the ones the server adds.

`Nats-` is a reserved prefix; use a different prefix for your own headers.

Publish-time headers (with the server version that introduced them):
- `Nats-Msg-Id`: client unique id; deduplicated within the stream `Duplicate Window` (2.2.0).
- `Nats-Expected-Stream`: assert the target stream (2.2.0).
- `Nats-Expected-Last-Msg-Id`, `Nats-Expected-Last-Sequence`: optimistic concurrency at stream level; publish is rejected on mismatch (2.2.0).
- `Nats-Expected-Last-Subject-Sequence`: same per subject (2.3.1); `Nats-Expected-Last-Subject-Sequence-Subject` lets that check use another subject, wildcards allowed (2.11.0).
- `Nats-Rollup`: `all` purges the whole stream, `sub` purges prior messages on that subject; the rollup message stays; stream needs rollups allowed; wildcard subjects give undefined behavior (2.6.2).
- `Nats-TTL`: per-message TTL such as `1h` or `10s`; stream needs per-message TTL enabled (2.11).

Server-added on republish or direct get (never set these yourself): `Nats-Stream`, `Nats-Subject`, `Nats-Sequence`, `Nats-Last-Sequence`, `Nats-Time-Stamp`, `Nats-Num-Pending`, `Nats-UpTo-Sequence`, `Nats-Stream-Source`.

Message scheduling headers (`Nats-Schedule`, `Nats-Schedule-Target`, `Nats-Schedule-TTL`) need a newer server and a stream with schedules enabled; the target must differ from the scheduling subject.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
