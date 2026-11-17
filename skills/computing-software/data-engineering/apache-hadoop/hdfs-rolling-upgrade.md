---
id: computing-software.data-engineering.apache-hadoop.hdfs-rolling-upgrade
name: hdfs-rolling-upgrade
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, rolling-upgrade, ha, datanode, downgrade]
level: sme
status: docs-checked
description: "HDFS rolling upgrade on an HA cluster: prepare, upgrade standby then active NameNode, DataNodes via shutdownDatanode, finalize; plus downgrade and rollback limits."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsRollingUpgrade.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rolling upgrade (HA)

1. Prepare: `hdfs dfsadmin -rollingUpgrade prepare`, then repeat `-rollingUpgrade query` until it says "Proceed with rolling upgrade."
2. Upgrade the standby NN2 and restart it with `namenode -rollingUpgrade started`; fail over to NN2; upgrade NN1 and restart it the same way.
3. DataNodes, in small batches (e.g. a rack): `hdfs dfsadmin -shutdownDatanode <HOST:IPC_PORT> upgrade`, poll `hdfs dfsadmin -getDatanodeInfo <HOST:IPC_PORT>` until it has shut down (the shutdown command does not wait), upgrade, restart.
4. Finalize: `hdfs dfsadmin -rollingUpgrade finalize`.

Federated clusters: prepare and finalize per namespace; DataNodes once.

Downgrade: DataNodes first, then NN2 (start normally), fail over, then NN1, then finalize. Only possible if layout versions are unchanged.

Rollback always needs downtime: stop all, restore old release, start NN1 with `namenode -rollingUpgrade rollback`, `-bootstrapStandby` NN2, start DataNodes with `-rollback`.

Limits: supported from 2.4.0; zero NameNode downtime needs HA; JournalNodes and ZooKeeper are not covered. Rollback is impossible after finalize or downgrade; downgrade is impossible after finalize. The `upgrade` option uses fast start-up; if the DataNode misses its window clients time out and fast start-up is disabled.

Non-HA clusters cannot upgrade without downtime because the NameNode must restart, but DataNodes can still roll. There the NN/SNN step is: shut down SNN, shut down and upgrade NN, start NN with `-rollingUpgrade started`, upgrade and restart SNN.

Data effects: a downgrade preserves user data (files created or deleted before or after the start time T stay that way). A rollback reverts to the pre-upgrade state: files created after T become unavailable and files deleted after T are restored. If a newer feature breaks on the old release, disable it, upgrade, then re-enable it. Downgrade DataNodes before NameNodes because old DataNodes can talk to new NameNodes but not vice versa. The `namenode -rollingUpgrade downgrade` options are obsolete.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (HdfsRollingUpgrade.md in the apache/hadoop repo). Procedure steps were accurate; added non-HA, data-effect and ordering details, and removed an unsupported "Verify" step.
