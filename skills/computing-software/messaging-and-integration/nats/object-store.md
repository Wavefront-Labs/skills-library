---
id: computing-software.messaging-and-integration.nats.object-store
name: object-store
category: computing-software
field: messaging-and-integration
product: nats
tags: [object-store, files, chunking, buckets]
level: practitioner
status: docs-checked
description: "Store arbitrarily large files in a JetStream Object Store bucket via chunking, with add/put/get/del/watch operations."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/nats-concepts/jetstream/object-store/obj_store.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move and store files of any size over NATS using JetStream.

An Object Store bucket corresponds to a stream. Files are stored and transmitted in chunks, so object size is not bounded by the server `max_payload`; the object is addressed by a path or file name used as the key.

Basic operations: `add` a bucket, `put` a file into it, `get` a file back to a designated location, `del` a file. Advanced: `watch` the bucket and receive notifications on successful `put` and `del`.

Important limitation stated in the docs: Object Store is not a distributed storage system. All files in a bucket must fit on the target file system of the node(s) holding the stream.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
