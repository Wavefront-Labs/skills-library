---
id: computing-software.database-administration.patroni.patroni-quorum-commit-mode
name: patroni-quorum-commit-mode
category: computing-software
field: database-administration
product: patroni
tags: [patroni, quorum, synchronous-mode, replication, sync-key]
level: advanced
status: docs-checked
description: "Quorum-based synchronous replication with synchronous_mode: quorum, how state is kept and what it changes."
sources:
  - https://patroni.readthedocs.io/en/latest/replication_modes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use quorum commit to cut worst-case write latency.

Quorum-based synchronous replication is supported from PostgreSQL v10. Enable it by setting `synchronous_mode` to `quorum` using `patronictl edit-config` or the REST API.

Patroni keeps in the DCS the latest known primary, the number of nodes required for quorum, and the nodes eligible to vote. In steady state the voters are the leader and all synchronous standbys. Updates happen with strict ordering relative to promotion and `synchronous_standby_names`, so any subset of voters that can reach quorum includes at least one node with the latest successful commit.

Each HA loop re-evaluates standby choice and quorum. Above PostgreSQL 9.6 all eligible nodes become synchronous standbys as soon as replication catches up. Benefit: a slow standby can be compensated by others, lowering worst-case latency even in normal operation.

`synchronous_node_count`, `maximum_lag_on_syncnode` and `synchronous_mode_strict` work as with `synchronous_mode=on`.

Example with `synchronous_node_count: 2`:

```
/sync: {"leader": "node0", "sync_standby": "node1,node2,node3", "quorum": 1}
synchronous_standby_names = 'ANY 2 (node1,node2,node3)'
```

If node0 fails, a node can be promoted without data loss if its LSN is not behind at least one of the other voters (quorum=1 here).

## Checked

2026-11-08. Confirmed against the Patroni replication modes page (quorum commit mode section and example). Removed the `failover_priority` limitation, which that page does not state.

Method: documentation only; no commands were run.
