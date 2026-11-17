---
id: computing-software.database-administration.yugabytedb.cluster-balancer-operations
name: cluster-balancer-operations
category: computing-software
field: database-administration
product: yugabytedb
tags: [cluster-balancer, load-balancer, enable-load-balancing, blacklist, leader-balancing, remote-bootstrap-rate-limit, yb-admin]
level: advanced
status: docs-checked
description: "Operate the YugabyteDB cluster balancer: check its state with yb-admin, pause it, watch its metrics, and set remote bootstrap throttling and upgrade flag cleanup."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb-sharding/cluster-balancing.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/admin/yb-admin.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/yb-master.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cluster balancer operations

The cluster balancer runs inside the master leader. It spreads tablet replicas and leaders across tservers, honours the placement policy, blacklists and preferred zones, and re-replicates after failures. `--enable_load_balancing` is true by default.

Commands:
```
yb-admin --master_addresses <masters> get_load_balancer_state
yb-admin --master_addresses <masters> get_is_load_balancer_idle
yb-admin --master_addresses <masters> set_load_balancer_enabled 0   # pause
yb-admin --master_addresses <masters> set_load_balancer_enabled 1
yb-admin --master_addresses <masters> get_load_move_completion
```
The Master UI has per-server peer and leader counts and blacklist state on the Tablet Servers tab, and (in 2024.2.6 and later, and 2025.1.1 and later) a Cluster Balancer view under Utilities > Load Balancer.

Metrics: `total_table_load_difference`, `blacklisted_leaders`, `tablets_in_wrong_placement` and `estimated_data_to_balance_bytes`.

Tuning:
- Replica moves use remote bootstrap, throttled in 2025.1.1 and later by `remote_bootstrap_rate_limit_bytes_per_sec`.
- After a node failure, leaders move in about 3 seconds, but re-replication waits `follower_unavailable_considered_failed_sec` (900).
- Scale-in: blacklist the node so replicas drain before you remove it.
- Legacy `load_balancer_*` flags (releases before 2025.1.1) are deprecated; after upgrading to a later release, unset them so the simpler defaults apply.

The cluster balancing page strongly recommends not disabling the balancer: while it is off the cluster cannot automatically re-replicate data after a node failure. If you pause it, re-enable it afterward.

The `remote_bootstrap_rate_limit_bytes_per_sec` flag is the tuning knob from release 2025.1.1; earlier releases have the legacy `load_balancer_*` flags. The limit applies to each node as sender and as receiver.

## Checked

2026-11-04. Confirmed against the cluster balancing architecture page (balancer inside YB-Master, scaling in by blacklisting, 3 second leader moves, 15 minute re-replication delay from `follower_unavailable_considered_failed_sec`, metrics `total_table_load_difference`, `blacklisted_leaders`, `tablets_in_wrong_placement`, `estimated_data_to_balance_bytes`, `enable_load_balancing` default true, legacy flags and the unset-after-upgrade warning) and the yb-admin reference (`get_load_balancer_state`, `get_is_load_balancer_idle`, `set_load_balancer_enabled`, `get_load_move_completion`). Removed the advice to pause the balancer for backups or upgrades, which no page supports, and added the page's warning against disabling it.

Method: documentation only; no commands were run.
