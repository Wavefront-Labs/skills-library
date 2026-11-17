---
id: computing-software.messaging-and-integration.nats.jetstream-source-and-mirror
name: jetstream-source-and-mirror
category: computing-software
field: messaging-and-integration
product: nats
tags: [source, mirror, replication, subject-transforms, leaf-nodes]
level: practitioner
status: docs-checked
description: "Replicate between JetStream streams with mirror (one origin, keeps sequences) or sources (many origins, filters, transforms)."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/nats-concepts/jetstream/source_and_mirror.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: asynchronously copy messages between streams, including across accounts, clusters and leaf nodes.

Both `mirror` and `sources` live on the receiving stream; the origin needs no configuration and needs no cleanup if the receiver goes away. They recover from connection loss and suit high latency or intermittent links.

Per-origin options: `Name` (origin stream), `StartSeq`, `StartTime`, `FilterSubject`, `SubjectTransforms` (Source and optional Destination; cannot be combined with `FilterSubject`) and `Domain` (JetStream domain of the origin, typical in hub and leaf topologies; the API prefix also supports leaf domains).

Mirror: exactly one origin, clients cannot publish to it, but messages may be deleted on demand and consumers work normally. Sequence numbers and timestamps are preserved.

Sources: one or more origins aggregated with local client writes into one interleaved stream. Sequence numbers are not retained, ordering within a single origin is kept, ordering between origins is undefined.

Gotchas:
- Deletes in the origin are NOT replicated.
- Changes in the target (deletes, publishes) do not flow back.
- For a read-only replica of a stream with sources, configure no listen subjects or deny publish through authorization.
- The target has its own retention, replication and storage.
- "Bring your own" sourcing takes `Name`, `Consumer.Name` and `Consumer.DeliverSubject`; other options move to that consumer, which must use the `AckFlowControl` ack policy.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
