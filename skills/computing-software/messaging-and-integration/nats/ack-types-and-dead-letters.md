---
id: computing-software.messaging-and-integration.nats.ack-types-and-dead-letters
name: ack-types-and-dead-letters
category: computing-software
field: messaging-and-integration
product: nats
tags: [ack, nak, term, in-progress, max-deliver, dead-letter, advisories]
level: practitioner
status: docs-checked
description: "Use Ack, AckSync, InProgress, Nak, Term, nakDelay and MaxDeliver advisories to implement redelivery and dead-letter handling."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/using-nats/developing-with-nats/js/consumers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control redelivery and build dead-letter handling with a JetStream consumer.

With explicit acks, the client can:
- `Ack()` success, or `AckSync()` to confirm the server received the ack;
- `inProgress()` to say more time is needed (resets the AckWait timer);
- `Nak()` for a temporary failure, requesting redelivery (immediate unless you pass `nakDelay()` / `NakWithDelay()`);
- `Term()` for a message that can never be processed, so it is not redelivered.

After each delivery an `AckWait` timer starts; it is cancelled by an Ack or Term and reset by InProgress. On expiry the server redelivers, with no guarantee it goes to the same client instance. Timing is controlled by `AckWait` or by the `BackOff` duration sequence, which overrides `AckWait`.

Dead-letter style handling: set `MaxDeliver`. When a message hits it, an advisory is published on `$JS.EVENT.ADVISORY.CONSUMER.MAX_DELIVERIES.<STREAM>.<CONSUMER>`; a `Term()` publishes `$JS.EVENT.ADVISORY.CONSUMER.MSG_TERMINATED.<STREAM>.<CONSUMER>`. Payload schemas: `nats schema info io.nats.jetstream.advisory.v1.max_deliver` and `...v1.terminated`; both carry `stream_seq`. Use the sequence to fetch the original message from the stream if you need its body.

In a WorkQueuePolicy stream, a message that reached MaxDeliver remains in the stream and must be deleted via the JetStream API.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
