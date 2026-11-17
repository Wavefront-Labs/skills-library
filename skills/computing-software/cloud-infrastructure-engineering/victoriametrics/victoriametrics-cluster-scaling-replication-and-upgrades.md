---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-cluster-scaling-replication-and-upgrades
name: victoriametrics-cluster-scaling-replication-and-upgrades
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [scaling, replication-factor, rebalancing, rolling-upgrade, vmstorage, vmctl-vm-native]
level: advanced
status: docs-checked
description: "Scale, replicate and upgrade a VictoriaMetrics cluster: adding vmstorage nodes, replicationFactor, rebalancing limits and restart order."
sources: ["https://docs.victoriametrics.com/victoriametrics/cluster-victoriametrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics cluster scaling replication and upgrades

Vertical scaling: components read CPU and memory limits only at startup, so restart after changing them.

Adding a vmstorage node:
1. Start it with the same `-retentionPeriod`.
2. Restart vmselect nodes with the new `-storageNode`.
3. Restart vminsert nodes with the new `-storageNode`.
The docs recommend at least 10 vmstorage nodes for load distribution and availability.

Scaling down: remove the node from vminsert `-storageNode` first. Keep it in vmselect until its data expires or is migrated with `vmctl vm-native` (using `--vm-intercluster`).

Rebalancing: the cluster does not rebalance historical data automatically. Either wait for retention to remove old data or send new data only to the new nodes while vmselect still reads all nodes.

Replication: `-replicationFactor=N` on vminsert stores N copies, so data stays available with up to N-1 vmstorage nodes down; you need at least `2*N-1` nodes. On vmselect set `-dedup.minScrapeInterval=1ms` when replication is on, and `-globalReplicationFactor` where applicable. Replication does not replace backups.

Upgrades:
- No downtime: restart nodes one by one in the order vmstorage, vminsert, vmselect (needs at least two of each).
- Minimum downtime: stop vminsert and vmselect in parallel, restart vmstorage in parallel, then start vminsert and vmselect in parallel.

Rolling restarts raise load on the remaining nodes by about `100%/(N-1)`; troubleshooting guidance suggests at least 8 vmstorage nodes, multiplied by the replication factor.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
