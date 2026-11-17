---
id: computing-software.data-engineering.apache-hadoop.hadoop-fs-rm-du-setrep
name: hadoop-fs-rm-du-setrep
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, fs-shell, rm, du, setrep, trash]
level: intro
status: docs-checked
description: "Option details for hadoop fs -rm, -du and -setrep: skipTrash, -safely with the 100 file limit, du columns and -x, setrep -w, and the fs.trash.interval requirement."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/FileSystemShell.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fs shell: rm, du, setrep

`hdfs dfs` is a synonym for `hadoop fs` on HDFS. rm, du and setrep return 0 on success and -1 on error.

rm: `hadoop fs -rm [-f] [-r|-R] [-skipTrash] [-safely] URI...`
- `-f`: no diagnostic and no error exit status if the file does not exist
- `-r` / `-R`: recursive
- `-skipTrash`: bypass trash and delete immediately (useful for over-quota directories)
- `-safely`: requires confirmation before deleting a directory with more files than `hadoop.shell.delete.limit.num.files` (default 100); counting a large tree causes a delay; can combine with `-skipTrash`
- Trash is disabled by default; enable it with `fs.trash.interval` greater than 0 in core-site.xml. With trash on, deletes move to the trash root; `-expunge` purges old checkpoints.
- `rmdir [--ignore-fail-on-non-empty]` deletes directories.

du: `hadoop fs -du [-s] [-h] [-v] [-x] URI...`
- Columns: size, disk space consumed with all replicas, full path
- `-s` aggregate summary (without it, one level deep); `-h` human sizes; `-v` header line; `-x` exclude snapshots (default counts all INodes, including snapshots)

setrep: `hadoop fs -setrep [-R] [-w] <numReplicas> <path>`
- On a directory, changes all files under it recursively; erasure-coded files are ignored
- `-w` waits for replication to complete (can take a very long time)
- `-R` is accepted for backwards compatibility and has no effect

Deprecated: `dus` (use `du -s`), `lsr` (use `ls -R`), `rmr` (use `rm -r`).

On object stores, trash would live in the bucket and keep incurring storage cost, so the page suggests `-skipTrash`; `setrep` has no effect there.

## Checked

Method: 2026-11-08 compared against the FileSystemShell page (apache/hadoop trunk markdown). Options and defaults match; added -f semantics, rmdir, object-store note, and removed the unsupported "Verify" step.
