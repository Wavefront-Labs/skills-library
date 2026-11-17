---
id: computing-software.cloud-infrastructure-engineering.etcd.data-model-mvcc
name: data-model-mvcc
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [data-model, mvcc, revisions, btree, flat-keyspace, history, storage-engine, generations]
level: advanced
status: docs-checked
description: "How etcd stores data: multi-version concurrency control, revisions, key generations, the persistent B+tree and the in-memory B-tree index."
sources:
  - "https://etcd.io/docs/v3.5/learning/data_model/"
  - "https://etcd.io/docs/v3.5/learning/api/"
  - "https://etcd.io/docs/v3.5/op-guide/maintenance/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

etcd is designed to reliably store infrequently updated data and provide reliable watch queries. It keeps previous versions of key-value pairs, which supports inexpensive snapshots and watch history ("time travel queries"). The store is effectively immutable: operations never update in place but generate a new structure, and all past versions stay accessible and watchable until compaction sheds the oldest superseded data.

Logical view:

- A flat binary key space with a lexically sorted index on byte-string keys, so range queries are inexpensive.
- Revisions: the initial revision is 1. Each atomic mutative operation (a transaction counts as one) creates a new revision; earlier revisions are unchanged and remain readable. Revisions only increase over the cluster's lifetime, and the store revision acts as a global logical clock. Compaction removes revisions before the compact revision.
- A key's life is a generation, from creation to deletion; a key may have many. Creating a key sets its version to 1, each modification increments it, and a deletion writes a tombstone and resets the version to 0. After compaction, generations that ended before the compaction revision are removed, and values before it except the latest are removed.

Physical view:

- Data is stored as key-value pairs in a persistent B+tree. Each revision holds only the delta from the previous one, and one revision may span several keys.
- The B+tree key is a 3-tuple (major, sub, type): major is the store revision, sub separates keys within one revision, and type is an optional suffix such as `t` for a tombstone. The tree is ordered by byte order, so ranged lookups over revision deltas are fast.
- A secondary in-memory B-tree index speeds up range queries over keys; its values point to modifications in the B+tree. etcd reads the revision from the B-tree, then fetches the value from the B+tree by revision. Compaction removes dead keys and pointers.

Operational consequences from the maintenance guide:

- Compaction leaves internal fragmentation in the backend database; only defragmentation returns that space to the filesystem.
- `etcd_mvcc_db_total_size_in_use_in_bytes` is actual usage after compaction; `etcd_mvcc_db_total_size_in_bytes` includes free space waiting for defragmentation. The space quota applies to the backend database.

## Checked

2026-11-08. Read the v3.5 data model page and API overview in full, and the maintenance guide (added as a source for the size metrics). Confirmed: logical and physical views, revisions, generations, tombstones, B+tree key tuple, in-memory B-tree index. Removed: bbolt naming and design advice, which the pages do not state.

Method: documentation only; no commands were run.
