---
id: computing-software.cloud-infrastructure-engineering.etcd.persistent-storage-files
name: persistent-storage-files
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [data-dir, wal, snap, db, snapshot-files, member-dir, persistent-storage, bbolt]
level: advanced
status: docs-checked
description: "What lives in an etcd data directory: member/snap/db, .snap files, WAL segments and temp files, and what each does."
sources:
  - "https://etcd.io/docs/v3.5/learning/persistent-storage-files/"
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `--data-dir` (default `${name}.etcd`) holds all persistent state under `member/`:

- `member/snap/db`: the bbolt b+tree that stores all applied data, membership and authorization information and metadata, including the last applied WAL index (`consistent_index`).
- `member/snap/{term}-{index}.snap`: periodic snapshots of the legacy v2 store (basic membership and etcd version); as of v3 the content is redundant with `snap/db`. They are purged periodically (30 s) and the last `--max-snapshots` (5) are kept.
- `member/snap/*.snap.db` and `member/snap/tmp*`: temporary files created on a replica while it retrieves a snapshot from the leader; after a complete download the file is renamed to `[SNAPSHOT-INDEX].snap.db`. If the server dies mid-download they are never cleaned up automatically and can be GBs (a cleanup fix landed in etcd 3.5).
- `member/snap/db.tmp.*`: temporary copy of the backend during defragmentation, renamed to `db` on success and pruned at startup.
- `member/wal/`: the write-ahead log, named `%016x-%016x.wal` (sequence, index of the first entry or snapshot); a new file is started when the current one exceeds 64*10^6 bytes. `0.tmp` / `1.tmp` is preallocated space for the next WAL file.

Behaviour:

- The leader stores each proposal in its WAL and replicates it; each follower persists the proposal in its WAL before confirming back to the leader. The WAL also holds Raft snapshots and hard state, so the member's whole Raft state can be recovered from it.
- `--snapshot-count` (default 100000) is the number of committed transactions that trigger a snapshot to disk.
- `--max-snapshots` (default 5) and `--max-wals` (default 5) keep that many files; 0 means unlimited.
- `--wal-dir` sets a dedicated WAL directory.

## Checked

2026-11-03. Confirmed on the v3.5 persistent storage files page: member/snap/db as the bbolt store with consistent_index, .snap files as legacy v2 store snapshots purged with --max-snapshots=5, .snap.db and tmp files for snapshot retrieval and the 3.5 fix, db.tmp during defragmentation, WAL file naming, the 64*10^6 byte cut size, preallocated .tmp files and the follower WAL persistence rule. Confirmed on the configuration page: --data-dir, --wal-dir, --snapshot-count 100000, --max-snapshots 5, --max-wals 5. Corrected: .snap files are v2 store snapshots, not Raft membership snapshots, and .snap.db files are not renamed to db. Removed: the purge-WAL, separate-device and remove-member-directory claims.

Method: documentation only; no commands were run.
