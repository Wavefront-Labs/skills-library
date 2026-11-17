---
id: computing-software.database-administration.yugabytedb.tablet-replica-limits
name: tablet-replica-limits
category: computing-software
field: database-administration
product: yugabytedb
tags: [tablet-limits, enforce-tablet-replica-limits, tablet-replicas-per-core-limit, tablet-replicas-per-gib-limit, split-respects-tablet-replica-limits, capacity]
level: advanced
status: docs-checked
description: "Cap the total tablet replicas a cluster accepts with enforce_tablet_replica_limits, per-core and per-GiB limits, and monitor the limit in the master UI and metrics."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb-sharding/tablet-splitting.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/yb-master.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tablet replica limits

Tablet limits make the master reject a CREATE TABLE (or a split) that would push the total replica count over what the cluster can support.

Configure:
1. Set `enforce_tablet_replica_limits` true on all YB-Masters.
2. Choose the resource basis. With YSQL the simplest route is `use_memory_defaults_optimized_for_ysql` true, which sets a sensible default for `tablet_overhead_size_percentage`. Otherwise set `tablet_replicas_per_core_limit` and/or `tablet_replicas_per_gib_limit` on all masters and tservers.
3. Optionally set `split_respects_tablet_replica_limits` true so automatic splits stop at the limit.

For YCQL-only clusters that do not reserve memory for YSQL, set `tablet_overhead_size_percentage` to 10 on all tservers.

Observe: in the Master UI, Tablet Servers tab, Universe Summary shows Active Tablet-Peers and Tablet Peer Limit. Metrics: `ts_supportable_tablet_peers` (-1 means no limit), `create_table_too_many_tablets` and `split_tablet_too_many_tablets`.

A rejected create returns an error such as: The requested number of tablet replicas (30) would cause the total running tablet replica count (102) to exceed the safe system maximum (93).

Known gap: tablets created in the second step of a YSQL restore are not checked against the limits. Disable the feature by setting `enforce_tablet_replica_limits` to false on all masters.

## Checked

2026-11-04. Confirmed against the tablet splitting architecture page and the yb-master reference: the enforce, per-core, per-GiB and split_respects flags, the Master UI Tablet Servers tab fields, the three metrics, the sample error, the restore gap, and tablet_overhead_size_percentage 10 for YCQL-only clusters. Reworded the memory-defaults sentence to what the page says.

Method: documentation only; no commands were run.
