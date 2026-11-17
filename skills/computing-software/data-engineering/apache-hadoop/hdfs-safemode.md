---
id: computing-software.data-engineering.apache-hadoop.hdfs-safemode
name: hdfs-safemode
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, safemode, namenode, startup]
level: practitioner
status: docs-checked
description: "What HDFS Safemode does at NameNode startup, when it exits on its own, and how to enter or leave it manually with hdfs dfsadmin -safemode."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safemode

On startup the NameNode loads the fsimage and edits log, then waits for DataNodes to report their blocks so it does not start replicating blocks that already have enough replicas. During this time it is in Safemode, essentially a read-only mode that allows no modification of the file system or blocks, and no replication of data blocks occurs.

DataNodes send Heartbeats and Blockreports. A block is safely replicated when its minimum number of replicas has checked in. After a configurable percentage of safely replicated blocks has checked in (plus an additional 30 seconds), the NameNode exits Safemode, works out which blocks still have too few replicas and replicates them to other DataNodes. Normally it leaves automatically.

Manual control: though usually not required, an administrator can enter or leave Safemode with `bin/hdfs dfsadmin -safemode`; the design page's example is `bin/hdfs dfsadmin -safemode enter`. The NameNode front page shows whether Safemode is on or off. Detailed threshold configuration is in the `setSafeMode()` JavaDoc, not on these pages.

Related: `bin/hdfs fsck` reports problems such as missing blocks or under-replicated blocks, but unlike a native fsck it does not correct them.

## Checked

Method: 2026-11-08 compared against the HDFS Design page and the HDFS User Guide (apache/hadoop trunk markdown). Startup behaviour and commands match; the draft's claims to enter Safemode before saveNamespace and to run fsck when the NameNode never exits were not on the pages and were dropped, as was the invented "Verify" step.
