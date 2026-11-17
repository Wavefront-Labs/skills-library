---
id: computing-software.data-engineering.apache-hadoop.hdfs-trash
name: hdfs-trash
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, trash, delete, skiptrash]
level: intro
status: docs-checked
description: "Where HDFS puts deleted files when trash is enabled, how checkpoints are named, and how to delete permanently with -skipTrash."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/FileSystemShell.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HDFS trash

If trash is enabled, files removed with the FS shell are not immediately removed; HDFS moves them to the user's trash directory under `/user/<username>/.Trash`, and they can be restored quickly while they remain there. The most recent deletions go to `/user/<username>/.Trash/Current`. At a configurable interval HDFS creates checkpoints under `/user/<username>/.Trash/<date>` for the files in Current and deletes expired checkpoints. After a file's life in trash expires, the NameNode deletes it from the namespace and its blocks are freed; free space may appear with a noticeable delay.

Trash is disabled by default; enable it by setting `fs.trash.interval` greater than 0 in core-site.xml. `hadoop fs -expunge [-immediate]` creates a checkpoint and purges old ones (`-immediate` empties the current user's trash).

The design page's example: `hadoop fs -rm -r delete/test1` prints "Moved: ... to trash at: .../.Trash/Current", and the file is then found by listing `.Trash/Current/user/hadoop/delete/`. To delete permanently and bypass trash:

```
hadoop fs -rm -r -skipTrash /path/to/dir
```

The page's example shows it printing "Deleted ...".

## Checked

Method: 2026-11-08 compared against the HDFS Design and FileSystemShell pages (apache/hadoop trunk markdown). Paths, checkpointing, `fs.trash.interval` and skipTrash match; the draft's "restore with mv" instruction and invented "Verify" step were not on the pages and were removed.
