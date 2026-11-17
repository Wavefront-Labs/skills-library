---
id: computing-software.data-engineering.apache-hadoop.hdfs-upgrade-and-rollback
name: hdfs-upgrade-and-rollback
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, upgrade, rollback, finalizeupgrade]
level: advanced
status: docs-checked
description: "Classic HDFS upgrade and rollback steps: start-dfs.sh -upgrade, finalizeUpgrade, namenode -rollback, saveNamespace, and renameReserved handling of .snapshot paths."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HDFS upgrade and rollback

HDFS can keep one upgrade backup at a time, allowing a rollback to the pre-upgrade state.

Before upgrading:
- Finalize any existing backup: `-finalizeUpgrade` (removes the backup made during the last upgrade; the page writes it as `bin/hadoop dfsadmin -finalizeUpgrade`, listed under `hdfs dfsadmin` elsewhere).
- Recommended where possible: `hdfs dfsadmin -saveNamespace`, because data inconsistency can result if an edit log operation refers to the destination of an automatically renamed file.
- Rename or delete paths reserved in the new version (`/.reserved`, `.snapshot` as a path component), or upgrade with `-upgrade -renameReserved [key=value pairs]`, e.g. `-upgrade -renameReserved .snapshot=.my-snapshot,.reserved=.my-reserved`. With no pairs, reserved paths get the suffix `.<LAYOUT-VERSION>.UPGRADE_RENAMED`. Otherwise the NameNode prints an error naming the reserved path.

Upgrade: stop the cluster, distribute the new Hadoop version, run with `sbin/start-dfs.sh -upgrade`.

Finalize once the new HDFS is considered working well (perhaps after a few days). Until then, deleting files that existed before the upgrade does not free real disk space on the DataNodes.

Rollback (to go back to the old version): stop the cluster, distribute the earlier version, run `bin/hdfs namenode -rollback` on the NameNode, then start with `sbin/start-dfs.sh -rollback`.

The page links a wiki page for fuller upgrade detail and does not cover HA clusters here.

## Checked

Method: 2026-11-08 compared against the HDFS User Guide upgrade section (apache/hadoop trunk markdown). Steps match; added the disk-space caveat and saveNamespace rationale, noted the finalize command spelling, and removed the invented "Verify" step and the reference to a rolling-upgrade page that this page does not make.
