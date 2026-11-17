---
id: computing-software.messaging-and-integration.nats.key-value-store
name: key-value-store
category: computing-software
field: messaging-and-integration
product: nats
tags: [key-value, kv, bucket, compare-and-set, watch]
level: practitioner
status: docs-checked
description: "Use the JetStream Key/Value store: buckets as KV_ streams, put/get/create/update, watch, history, limits, and consistency caveats."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/nats-concepts/jetstream/key-value-store/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use JetStream as a consistent, persistent map with change notifications.

A KV bucket is an abstraction over a stream; the stream name starts with `KV_`, so anything the KV API does you can also do with stream features.

Operations:
- Map style: put, get, delete, purge (clear all values for all keys), keys.
- Atomic: `create` (set only if the key has no value) and `update` (compare and set) give locking and concurrency control.
- Stream style: `watch` a key, `watch all` keys, `history` of values and deletes. Bucket history defaults to 1, meaning only the latest value is kept.
- Limits: maximum bucket size, maximum value size, and a TTL for values.

Keys may contain letters, digits, `_`, `-`, `.`, `=` and `/`; dot-separated tokens allow wildcard watches across a hierarchy. Values are arbitrary bytes.

Consistency gotcha: monotonic reads and writes are guaranteed, but read-your-writes is not, because direct get requests can be answered by followers or mirrors. For stronger results send gets to the underlying stream leader.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
