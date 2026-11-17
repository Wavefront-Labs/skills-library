---
id: computing-software.database-administration.valkey.replication-safety-and-writes
name: replication-safety-and-writes
category: computing-software
field: database-administration
product: valkey
tags: [replication-safety, min-replicas-to-write, min-replicas-max-lag, writable-replica, persistence-off, expires]
level: advanced
status: docs-checked
description: "Valkey replication safety: primaries without persistence wiping replicas, writable replicas, min-replicas-to-write, and how expires replicate."
sources:
  - https://valkey.io/topics/replication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Persistence-off hazard: if primary A has no persistence and auto-restarts after a crash, it returns empty and replicas B and C replicate the empty dataset, wiping their copies. Any one fix suffices: turn persistence on everywhere; do not auto-restart crashed instances; or replace the node with a new instance. Cluster is safe with replacement because node IDs are fresh. Sentinel identifies instances by address, so a replacement reusing the address looks like a reboot; it logs `+reboot` but does not fail over, and `primary-reboot-down-after-period` only forces failover while the primary stays unresponsive.

Writable replicas are historical and discouraged: propagated commands (a `DEL` for an expired key, `INCR`, `RPOP`) may behave differently on diverged keys. Replica writes are local, never forwarded to sub-replicas (in A to B to C, C ignores B writes) and vanish on resync. Alternatives since 7.0: `SUNION`/`ZINTER` instead of `*STORE`, `SORT_RO`, `EVAL_RO`/`EVALSHA_RO`.

Bounded loss: `min-replicas-to-write <n>` with `min-replicas-max-lag <seconds>` makes the primary reject writes unless at least n replicas have a lag at most that many seconds (replicas ping each second with their offset). It limits the loss window but cannot guarantee delivery.

Expires: clocks are not synced, so replicas do not expire keys; the primary expires or evicts and sends `DEL`. Meanwhile replicas hide logically expired keys from reads. No key expires while a script runs (time is frozen). A promoted replica expires keys itself.

Inspect with `INFO replication` and `ROLE`.

## Checked
2026-11-03. Confirmed against the Valkey Replication page (valkey.io/topics/replication/): the persistence-off wipe scenario and its three fixes, Cluster node IDs versus Sentinel address identification, `+reboot` and `primary-reboot-down-after-period`, writable replica hazards and the 7.0 alternatives (SUNION/ZINTER, SORT_RO, EVAL_RO/EVALSHA_RO), local-only replica writes, `min-replicas-to-write` and `min-replicas-max-lag`, and the expiry rules including frozen time during scripts. Nothing removed.
Method: documentation only; no commands were run.
