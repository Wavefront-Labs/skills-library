---
id: computing-software.database-administration.valkey.replication-full-sync-tuning
name: replication-full-sync-tuning
category: computing-software
field: database-administration
product: valkey
tags: [full-sync, repl-diskless-sync, repl-diskless-load, dual-channel-replication, repl-compression, replication-tuning]
level: advanced
status: docs-checked
description: "Valkey full resynchronization tuning: repl-diskless-sync and delay, repl-diskless-load modes, dual-channel replication (8.0) and repl-compression (9.2)."
sources:
  - https://valkey.io/topics/replication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A full sync always sends an RDB-format snapshot, but it need not touch disk; primary and replica sides are configured independently.

Primary: diskless is default (`repl-diskless-sync yes`); the child streams to the socket using a random end-of-file marker. The primary waits `repl-diskless-sync-delay` (5 s default; 0 starts at once) so arriving replicas share one snapshot; `repl-diskless-sync-max-replicas` caps replicas per transfer (0 = no limit). With `repl-diskless-sync no` it saves the RDB and sends the file, shareable by replicas that arrive during the save. Replicas needing a filtered dataset, older RDB version or other compression codec still get a diskless transfer.

Replica `repl-diskless-load`: `disabled` (default; write to a temporary file then load), `on-empty-db` (load from socket only if the dataset is empty), `swapdb` (keep old data in memory while loading; needs memory for both or risks OOM kill), `flush-before-load` (dangerous: deletes data first).

Dual-channel replication (since 8.0): the replica opens a second connection to accumulate the write stream while the snapshot flows on the first, moving buffering memory from primary to replica. Set `dual-channel-replication-enabled yes` on both, and `repl-diskless-sync` must be on the primary.

Compression (since 9.2): `repl-compression` is `no` (default), `yes` (currently LZ4), `lz4`, or `zstd` (needs build support). Set on both sides; each value is the strongest algorithm that side accepts, and the link uses the strongest common one (zstd primary with lz4 replica gives lz4). It covers the diskless payload and the command stream. Keep it equal to `rdbcompression` so disk-based sync stays possible.

## Checked
2026-11-03. Confirmed against the Valkey Replication page (valkey.io/topics/replication/): RDB-format full sync, diskless default, `repl-diskless-sync-delay` (5 s) and `repl-diskless-sync-max-replicas` (0 means no limit), disk-based sharing and the filtered/older-version/other-codec exceptions, the four `repl-diskless-load` modes, dual-channel replication since 8.0 and its requirements, and `repl-compression` since 9.2 with its negotiation rules. Nothing removed.
Method: documentation only; no commands were run.
