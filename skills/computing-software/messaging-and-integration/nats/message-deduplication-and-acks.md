---
id: computing-software.messaging-and-integration.nats.message-deduplication-and-acks
name: message-deduplication-and-acks
category: computing-software
field: messaging-and-integration
product: nats
tags: [deduplication, nats-msg-id, dupe-window, ack-modes, ack-floor, exactly-once]
level: practitioner
status: docs-checked
description: "Get idempotent JetStream writes with Nats-Msg-Id and the 2-minute duplicate window; understand stream and consumer ack modes."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/using-nats/jetstream/model_deep_dive.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid duplicate stored messages and read consumer ack state correctly.

Deduplication: set a `Nats-Msg-Id` header on publish and JetStream ignores later messages carrying the same id, comparing only the id and not the body. Example from the page: four `nats req -H Nats-Msg-Id:1 ORDERS.new helloN` calls leave one stored message (see `nats stream info ORDERS`, State Messages 1). The tracking window defaults to 2 minutes and is set when creating a stream with `--dupe-window`; the docs caution against large windows.

Stream acknowledgements: a request (not a plain publish) to a subject the stream covers gets a reply once the message is stored. Setting `NoAck` to true on the stream disables that.

Consumer ack modes:
- `AckExplicit`: every message acknowledged individually; the only supported mode for pull consumers.
- `AckAll`: acking message 100 also acks 1 to 99, reducing ack traffic for batches.
- `AckNone`: no acks.
- `AckFlowControl` (2.14): acks follow flow control, mainly for sourcing and mirroring with a durable consumer.

Reading `nats consumer info <stream> <consumer>`: the acknowledgment floor is the last contiguously acked consumer and stream sequence; Pending Messages counts delivered but unacked messages; Redelivered Messages counts retries. In the page's walkthrough, fetching with `nats consumer next ORDERS DISPATCH --no-ack` leaves the floor unchanged and pending at 1.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
