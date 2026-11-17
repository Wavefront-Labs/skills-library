---
id: computing-software.cloud-infrastructure-engineering.etcd.watch-api-semantics
name: watch-api-semantics
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [watch, watch-api, events, progress-notify, filters, compact-revision, watch-id]
level: advanced
status: docs-checked
description: "The Watch gRPC API: create requests, start revision, filters, prev_kv, progress notify, compaction responses and the event guarantees."
sources:
  - "https://etcd.io/docs/v3.5/learning/api/"
  - "https://etcd.io/docs/v3.5/learning/api_guarantees/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The Watch API streams key changes over a bidirectional gRPC stream: the client writes to the stream to establish watches and reads to receive events. One stream can multiplex many watches by tagging events with per-watch identifiers, which reduces memory and connection overhead on the cluster.

A `WatchCreateRequest` has:

- `key` and `range_end`: the key range to watch.
- `start_revision`: optional, where to inclusively begin watching. If not given, events stream from the revision of the watch creation response header. The whole available history can be watched from the last compaction revision.
- `progress_notify`: when set, the watch periodically receives a `WatchResponse` with no events if there are no recent events. The server decides how often, based on load. It helps recover a disconnected watcher from a recent known revision.
- `filters`: event types to drop server-side (NOPUT, NODELETE).
- `prev_kv`: include the key-value data from before the event.

A client stops a watch with a `WatchCancelRequest` carrying the `watch_id`.

Each `Event` has a type (PUT or DELETE), `kv` and optionally `prev_kv`. A PUT with `kv.Version=1` means the key was created; a DELETE carries the deleted key with its modification revision set to the revision of deletion. Expired lease keys generate delete events.

A `WatchResponse` carries the header, `watch_id`, `created`, `canceled`, `compact_revision` and `events`. `compact_revision` is set to the minimum historical revision available when a watcher tries a compacted revision, either at creation or because it cannot keep up; that watcher is canceled and new watches with the same `start_revision` fail.

Guarantees (API guarantees page): events are ordered by revision, unique, reliable (no gaps within the available history window), atomic (a list of events holds complete revisions), resumable (start a new watch after the last revision received, while it is still in the history window) and bookmarkable (progress notifications guarantee all events up to a revision were delivered).

Caveats: etcd does not ensure linearizability for watches, so compare event revisions to order them against other operations. Events normally arrive within about 10ms but there is no bound, and in an unhealthy cluster they might never arrive.

## Checked

2026-11-08. Read the v3.5 API overview and API guarantees pages in full. Confirmed: WatchCreateRequest fields, WatchResponse fields, compact_revision behaviour, event semantics and the six watch guarantees. Removed: watch_id and fragment create fields, the empty-response-with-revision description of progress notify and the full re-list pattern, none stated on the pages. Added: non-linearizability and delay caveat.

Method: documentation only; no commands were run.
