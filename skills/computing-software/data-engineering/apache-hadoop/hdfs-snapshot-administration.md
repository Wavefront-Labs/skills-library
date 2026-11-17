---
id: computing-software.data-engineering.apache-hadoop.hdfs-snapshot-administration
name: hdfs-snapshot-administration
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, snapshots, allowsnapshot, backup]
level: practitioner
status: docs-checked
description: "Creating, renaming, deleting and listing HDFS snapshots: allowSnapshot, createSnapshot defaults, the .snapshot path, and the 65,536 per-directory limit."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsSnapshots.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HDFS snapshots

Read-only point-in-time copies of a subtree or the whole file system, used for backup, protection against user errors and disaster recovery. Creation is O(1) excluding inode lookup, extra memory is used only for modifications relative to a snapshot, and datanode blocks are not copied.

Superuser operations:

```
hdfs dfsadmin -allowSnapshot <path>
hdfs dfsadmin -disallowSnapshot <path>        # all snapshots must be deleted first
hdfs dfsadmin -provisionSnapshotTrash <path> [-all]
```

`-provisionSnapshotTrash` provisions a trash root in the directory, or in all snapshottable directories with `-all`.

User operations (create, delete and rename need owner privilege on the snapshottable directory; the HDFS superuser can do everything):

```
hdfs dfs -createSnapshot <path> [<snapshotName>]
hdfs dfs -renameSnapshot <path> <oldName> <newName>
hdfs dfs -deleteSnapshot <path> <snapshotName>
hdfs lsSnapshottableDir         # directories where you may take snapshots
hdfs lsSnapshot <snapshotRoot>  # snapshots of a directory
```

With no name, createSnapshot generates one in the format `s20130412-151029.033` (`'s'yyyyMMdd-HHmmss.SSS`).

Read snapshot contents through the `.snapshot` path component, e.g. `/foo/.snapshot/s0/bar`; the usual API and CLI work on it. Examples on the page: `hdfs dfs -ls /foo/.snapshot`, and `hdfs dfs -cp -ptopax /foo/.snapshot/s0/bar /tmp` (preserving timestamps, ownership, permission, ACLs and XAttrs).

Constraints: up to 65,536 simultaneous snapshots per snapshottable directory; no limit on the number of snapshottable directories; nested snapshottable directories (ancestor or descendant) are not allowed; a directory with snapshots can be neither deleted nor renamed until they are deleted. Upgrading from a release without snapshots: rename or delete existing paths named `.snapshot` first.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (HdfsSnapshots.md in the apache/hadoop repo). Added lsSnapshot, provisionSnapshotTrash and permission details; removed an unsupported "Verify" step. Remaining claims were accurate.
