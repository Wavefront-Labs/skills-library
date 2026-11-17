---
id: computing-software.data-engineering.apache-hadoop.hdfs-snapshot-diff
name: hdfs-snapshot-diff
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, snapshots, snapshotdiff, change-detection]
level: advanced
status: docs-checked
description: "Reading hdfs snapshotDiff reports: the +, -, M, R codes, comparing to current state with a dot, rename edge cases, and required read access."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsSnapshots.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# snapshotDiff

```
hdfs snapshotDiff <path> <fromSnapshot> <toSnapshot>
```

`path` is the snapshottable directory. It reports differences between two snapshots, or between a snapshot and the current state of the directory, where "." represents the current state. The caller needs read access to all files and directories in both snapshots. Java equivalent: `SnapshotDiffReport getSnapshotDiffReport(Path, String, String)` in `DistributedFileSystem`.

Result codes:
- `+` created
- `-` deleted
- `M` modified
- `R` renamed

Edge cases:
- A rename that stays under the same snapshottable directory is an `R` entry.
- A file or directory renamed to outside the snapshottable directory is reported as deleted; one renamed in from outside is reported as newly created.
- The report does not guarantee the same operation sequence. Page example: rename `/foo` to `/foo2`, then append to `/foo2/bar`, giving `R. /foo -> /foo2` and `M. /foo/bar`; changes under a renamed directory are reported with the original path from before the rename.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (HdfsSnapshots.md in the apache/hadoop repo). Removed an unsupported "Verify" recipe and editorial advice about replay logic; codes and edge cases were accurate.
