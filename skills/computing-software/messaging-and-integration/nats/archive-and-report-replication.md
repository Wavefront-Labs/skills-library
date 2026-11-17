---
id: computing-software.messaging-and-integration.nats.archive-and-report-replication
name: archive-and-report-replication
category: computing-software
field: messaging-and-integration
product: nats
tags: [replication, archive-stream, mirror, sources, nats-s-add, topology]
level: practitioner
status: docs-checked
description: "Build a fan-in archive stream with --source and a read-only report mirror using the nats CLI; ordering and listen-subject rules."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/nats_admin/jetstream_admin/replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replicate data between streams in mirror style or by multiplexing several sources.

The page example: two clustered, memory-backed, short-retention streams ORDERS and RETURNS feed an ARCHIVE stream with two sources (long retention, file storage, replicated), and a REPORT stream mirrors ARCHIVE (not clustered, one month retention, no listen subjects so it only consumes from ARCHIVE).

Commands:
- `nats s report` shows stream storage, messages and the cluster peers (leader starred).
- `nats s add ARCHIVE --source ORDERS --source RETURNS` prompts for storage, retention, discard, limits, duplicate window (default 2m0s) and, per source, start sequence, UTC start time, subject filter, JetStream domain and account import.
- `nats s add REPORT --mirror ARCHIVE`.
- When creating sourced streams that should also accept direct writes, pass `--subjects`.

Semantics:
- A mirror copies from exactly one stream, IDs and ordering match as far as possible, does not listen on subjects, can filter by subject, and has Start Sequence or Start Time. A stream can only have one mirror.
- A stream with sources reads from all of them and may also listen on its own subjects, so absolute order across sources is not maintained; order from any single source is preserved.
- Extra messages can be published straight into the archive stream.

Gotcha: the page notes cross-account replication was future work at the time of writing; use the account import options in the sourcing prompts and the stream sourcing page instead.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
