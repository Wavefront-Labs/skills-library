---
id: computing-software.database-administration.patroni.patroni-synchronous-node-count-and-lag
name: patroni-synchronous-node-count-and-lag
category: computing-software
field: database-administration
product: patroni
tags: [patroni, synchronous-node-count, maximum-lag-on-syncnode, sync-standby, replication]
level: advanced
status: docs-checked
description: "Control how many synchronous standbys Patroni keeps and when it swaps a lagging one."
sources:
  - https://patroni.readthedocs.io/en/latest/replication_modes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage the synchronous standby set.

- `synchronous_node_count` (default 1): with synchronous mode on, Patroni manages exactly that many synchronous standbys and updates the DCS state and `synchronous_standby_names` as members join and leave. If it exceeds the number of eligible nodes, it is reduced automatically. It has no effect when `synchronous_mode` is off.
- `maximum_lag_on_syncnode`: by default Patroni sticks to nodes declared synchronous in `pg_stat_replication`, even when others are ahead, to minimise changes to `synchronous_standby_names`. Setting this value makes a synchronous standby that lags more than this many bytes be swapped for a healthy asynchronous one. Patroni measures against the max replica LSN if there are several standbys, otherwise the leader's WAL LSN. Default -1; 0 or below disables swapping. Set it high enough to avoid frequent swaps under heavy transaction volume.
- Tags: `nosync: true` means never synchronous; `sync_priority` (integer) prefers higher values when `synchronous_mode` is on, and 0 or negative excludes the node from `synchronous_standby_names`. Its meaning is opposite to `sync_priority` in `pg_stat_replication`.

Selection on each HA loop: a currently connected synchronous standby that has not asked to be removed stays; otherwise the available members furthest ahead in replication are picked.

Example state: `synchronous_node_count: 2` yields `synchronous_standby_names = 'FIRST 2 (node1,node2)'` and a `/sync` DCS key listing the leader and sync standbys.

## Checked

2026-11-03. Confirmed against the replication modes page and Dynamic Configuration (synchronous_node_count, maximum_lag_on_syncnode) and YAML Configuration Settings (nosync, sync_priority tags).

Method: documentation only; no commands were run.
