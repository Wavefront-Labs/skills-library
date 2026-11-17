---
id: computing-software.data-engineering.apache-hadoop.hdfs-namenode-checkpoint-triggers
name: hdfs-namenode-checkpoint-triggers
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, namenode, fsimage, editlog, checkpoint]
level: practitioner
status: docs-checked
description: "HDFS FsImage and EditLog roles, and the two properties that trigger a checkpoint: dfs.namenode.checkpoint.period and dfs.namenode.checkpoint.txns, plus who performs it."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NameNode checkpointing

The FsImage holds the entire namespace, including the block-to-file mapping and file properties. The EditLog is a transaction log recording every metadata change. A checkpoint applies the EditLog to the FsImage, writes a new FsImage, and lets the old EditLog be truncated; the page explains that editing the FsImage directly is inefficient, so edits go to the log. A checkpoint also runs when the NameNode starts.

Triggers (design page: if both are set, the first threshold reached triggers a checkpoint):
- `dfs.namenode.checkpoint.period`: maximum delay between two consecutive checkpoints, in seconds, 1 hour by default.
- `dfs.namenode.checkpoint.txns`: uncheckpointed transactions that force an urgent checkpoint even if the period has not elapsed, 1 million by default.

Who checkpoints:
- Secondary NameNode: merges fsimage and edits periodically to keep the edits log bounded; usually on a different machine since its memory needs match the NameNode's. It keeps the latest checkpoint in a directory laid out like the NameNode's.
- Checkpoint node: `bin/hdfs namenode -checkpoint`; it downloads fsimage and edits from the active NameNode, merges them and uploads the new image back. Multiple checkpoint nodes may be configured. Location set by `dfs.namenode.backup.address` and `dfs.namenode.backup.http-address`.
- Backup node: `bin/hdfs namenode -backup`; also keeps an in-memory, synchronised copy of the namespace so its RAM need equals the NameNode's, and checkpoints without downloading files. The NameNode supports one Backup node at a time, and no Checkpoint nodes may be registered while one is in use.

Import Checkpoint: if all image and edits copies are lost, start the NameNode with `-importCheckpoint` after creating an empty `dfs.namenode.name.dir` and pointing `dfs.namenode.checkpoint.dir` at the checkpoint; it fails if a legal image is already in name.dir.

The NameNode can keep multiple copies of FsImage and EditLog, updated synchronously (which may reduce namespace transactions per second); on restart it selects the latest consistent copies.

## Checked

Method: 2026-11-08 compared against the HDFS Design and User Guide pages (apache/hadoop trunk markdown). Triggers, defaults and node roles match; the unsupported "run saveNamespace before an upgrade" line was moved out (it belongs to the upgrade skill) and the invented "Verify" step removed.
