---
id: computing-software.messaging-and-integration.nats.jetstream-stream-config
name: jetstream-stream-config
category: computing-software
field: messaging-and-integration
product: nats
tags: [jetstream, stream-config, retention, discard-policy, placement]
level: practitioner
status: docs-checked
description: "Configure JetStream streams: storage, replicas, limits, retention (limits, interest, work-queue), discard, placement tags, editable fields."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/nats-concepts/jetstream/streams.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define a stream that captures subjects with the right limits and retention.

Core fields (names as in the docs table): `Name` (unique per account; no whitespace, `.`, `*`, `>`, slashes), `Subjects` (wildcards allowed; defaults to the stream name; not allowed on a mirror), `Storage` (`File` default, or `Memory`), `Replicas` (max 5), `MaxAge` (nanoseconds), `MaxBytes`, `MaxMsgs`, `MaxMsgSize` (payload plus headers), `MaxMsgsPerSubject`, `MaxConsumers`, `DuplicateWindow`, `NoAck` (needed when archiving request messages that carry reply subjects), `Compression` (`s2`), `Placement`.

Not editable after creation: `Name`, `Storage`, `Retention`, `MaxConsumers`, `DenyDelete`, `DenyPurge`. `Sealed` can be set once through update and never unset.

Retention: `LimitsPolicy` (default; first limit hit wins), `WorkQueuePolicy` (message deleted on ack; only one consumer per subject, filters must not overlap), `InterestPolicy` (deleted once all interested consumers ack; with zero consumers published messages are dropped immediately). Limits still apply on top of the other two policies.

Discard: `DiscardOld` (default) or `DiscardNew`; `DiscardNewPerSubject` needs DiscardNew plus `MaxMsgsPerSubject`.

Placement uses a cluster name and/or server tags; with `jetstream.unique_tag: "az"` replicas land in different tag values. Example: `nats stream add --tag region:us-east1`.

Gotcha: in a WorkQueue stream, messages that hit `MaxDeliver` stay and must be deleted via the API.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
