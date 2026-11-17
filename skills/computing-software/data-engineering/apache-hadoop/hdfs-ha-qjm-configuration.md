---
id: computing-software.data-engineering.apache-hadoop.hdfs-ha-qjm-configuration
name: hdfs-ha-qjm-configuration
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, high-availability, qjm, journalnode, namenode]
level: advanced
status: docs-checked
description: "HDFS HA with Quorum Journal Manager: hdfs-site keys for nameservices, NameNode IDs, shared edits, failover proxy, JournalNode sizing and initialization commands."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HDFS HA with QJM

hdfs-site.xml keys:
- `dfs.nameservices`: logical name, e.g. `mycluster`.
- `dfs.ha.namenodes.<ns>`: NameNode IDs, e.g. `nn1,nn2` (minimum two; three recommended, no more than five).
- `dfs.namenode.rpc-address.<ns>.<nn>`: e.g. `machine1.example.com:8020`; a parallel http-address key sets the web port.
- `dfs.namenode.shared.edits.dir`: `qjournal://host1:8485;host2:8485;host3:8485/<journalId>`, set on one value only.
- `dfs.client.failover.proxy.provider.<ns>`: `ConfiguredFailoverProxyProvider` or `RequestHedgingProxyProvider`.
- `dfs.journalnode.edits.dir`: single absolute local path.

core-site.xml: optional `fs.defaultFS` such as `hdfs://mycluster`.

JournalNodes: run at least three, odd counts preferred; N nodes tolerate (N-1)/2 failures. Start with `hdfs --daemon start journalnode`.

The JournalNode default port is 8485. The page suggests reusing the nameservice ID as the journal ID, and says `dfs.namenode.edits.qjournals.resolution-enabled` plus a round-robin DNS record can avoid hardcoded names. Edits go to a majority of JournalNodes and only one NameNode is allowed to write, so a split brain cannot corrupt metadata. In an HA cluster the standby checkpoints, so do not run a Secondary NameNode, CheckpointNode or BackupNode.

Initialisation (after starting the JournalNodes):
- Fresh cluster: `hdfs namenode -format` on one NameNode.
- Already formatted, or converting a non-HA cluster: `hdfs namenode -bootstrapStandby` on the unformatted NameNode(s), which also ensures the JournalNodes hold enough edits to start both.
- Converting a non-HA NameNode: `hdfs namenode -initializeSharedEdits` initialises the JournalNodes from the local edits directories.

Every NameNode starts as Standby; the web UI shows its HA state next to its address. Operate with `hdfs haadmin`: `-getServiceState <id>`, `-getAllServiceState`, `-failover [--forcefence] [--forceactive] <id1> <id2>` (graceful, then fencing methods in order; the second NameNode is not made active if none succeeds) and `-checkHealth` (not yet implemented; returns success unless the NameNode is down). `-transitionToActive/Standby` do no fencing and should rarely be used. For load balancers, `/isActive` returns 200 on the active NameNode and 405 otherwise.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (HDFSHighAvailabilityWithQJM.md in the apache/hadoop repo). Corrected the initialisation sequence to match the page's three cases and removed an unsupported "Verify" step. Config keys were accurate.
