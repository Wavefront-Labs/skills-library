---
id: computing-software.data-engineering.apache-hadoop.hdfs-datanode-decommission-maintenance
name: hdfs-datanode-decommission-maintenance
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, datanode, decommission, maintenance, refreshnodes]
level: advanced
status: docs-checked
description: "Decommissioning and maintenance for HDFS DataNodes: admin states, dfs.hosts files in hostname or JSON format, refreshNodes, tuning keys and the backoff monitor."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDataNodeAdminGuide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DataNode admin

Admin states: NORMAL, DECOMMISSION_INPROGRESS, DECOMMISSIONED, ENTERING_MAINTENANCE, IN_MAINTENANCE. Maintenance is lighter: the node needs only minimal replication elsewhere and can auto-return after a timeout.

Two steps: edit host files, then `hdfs dfsadmin -refreshNodes`.

Formats:
- Hostname-only (default): `dfs.hosts` and `dfs.hosts.exclude`. Decommission and recommission only.
- JSON: set `dfs.namenode.hosts.provider.classname` to `CombinedHostFileManager` and point `dfs.hosts` at the JSON file. Required for maintenance. Fields: `hostName` (required), `upgradeDomain`, `adminState` (default NORMAL), `port`, `maintenanceExpireTimeInMS` (epoch ms, default no expiry).

Cluster settings (defaults in hdfs-default.xml): `dfs.namenode.maintenance.replication.min`, `dfs.namenode.decommission.interval`, `dfs.namenode.decommission.blocks.per.interval`, `dfs.namenode.decommission.max.concurrent.tracked.nodes`.

Experimental, disabled by default: set `dfs.namenode.decommission.monitor.class` to `org.apache.hadoop.hdfs.server.blockmanagement.DatanodeAdminBackoffMonitor` (HDFS-14854) in hdfs-site.xml. It addresses the original algorithm's issues when decommissioning DataNodes with many blocks: a long-held NameNode write lock while queueing re-replication, and re-replication progressing node by node. Related keys: `dfs.namenode.decommission.backoff.monitor.pending.limit` and `...pending.blocks.per.lock`.

Decommission: the node goes to DECOMMISSION_INPROGRESS, then DECOMMISSIONED once all its blocks are fully replicated elsewhere per replication factor; only then can it be shut down for long repairs, and later recommissioned. Maintenance: ENTERING_MAINTENANCE moves to IN_MAINTENANCE as soon as its blocks are minimally replicated elsewhere; for `adminState` use `DECOMMISSIONED` or `IN_MAINTENANCE`.

Check states: NameNode web UI, JMX, `hdfs dfsadmin -report`, and `hdfs fsck <path>` (shows decommission state only; add `-maintenance` to include maintenance state).

## Checked

Method: 2026-11-08 docs-only read of the page's source file (HdfsDataNodeAdminGuide.md in the apache/hadoop repo). Claims were accurate; added state transitions and backoff monitor background, and replaced an unsupported "Verify" line with the page's stated transitions.
