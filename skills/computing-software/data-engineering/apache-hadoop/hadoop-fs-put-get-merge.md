---
id: computing-software.data-engineering.apache-hadoop.hadoop-fs-put-get-merge
name: hadoop-fs-put-get-merge
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, fs-shell, put, get, getmerge, appendtofile, cp]
level: intro
status: docs-checked
description: "Moving data with hadoop fs: put flags (-f -p -l -d -t -q), cp -p[topax], get, getmerge -nl, appendToFile, concat and object store caveats."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/FileSystemShell.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fs shell: copying data

put: `hadoop fs -put [-f] [-p] [-l] [-d] [-t <threads>] [-q <queue size>] [ - | <localsrc>...] <dst>` (`copyFromLocal` is identical)
- `-f` overwrite (otherwise copying fails if the file exists); `-p` preserve times, ownership, permissions
- `-l` lazy persist: lets the DataNode persist lazily and forces replication 1, reducing durability
- `-d` skip the temporary `._COPYING_` file
- `-t` threads (default 1, useful for directories); `-q` queue size (default 1024, only with more than one thread)
- source `-` reads stdin
- `moveFromLocal` is like put but deletes the local source.

cp: `hadoop fs -cp [-f] [-p | -p[topax]] [-d] [-t n] [-q n] URI... <dest>`. `-p` alone preserves timestamps, ownership, permission; `-pa` also preserves permission since ACL is a superset. Multiple sources need a directory destination.

get (`copyToLocal` is identical): `hadoop fs -get [-ignoreCrc] [-crc] [-p] [-f] [-t n] [-q n] <src>... <localdst>`.

getmerge: `hadoop fs -getmerge [-nl] [-skip-empty-file] <src> <localdst>`; `-nl` adds a newline (LF) after each file, `-skip-empty-file` avoids stray newlines for empty files.

appendToFile: `hadoop fs -appendToFile [-n] <localsrc>... <dst>`; `-` reads stdin; `-n` uses the NEW_BLOCK create flag; exits 0 or 1.

concat: `hadoop fs -concat <target> <sources>`; target and sources should be in the same directory.

mv does not work across file systems.

Object stores (S3, ABFS, GCS): rename takes time proportional to data size and most shell operations end with a rename, so use `put -d` / `copyFromLocal -d` for a direct upload. The page lists `appendToFile`, `truncate`, `concat` and the snapshot commands as generally unsupported there, `setrep` as having no effect, and `chmod`/`chown`/`chgrp` as no-ops. `-p` does not preserve permissions on object stores (wasb preserves but does not enforce them). `cp` reads and rewrites each object; distance from the store slows it.

## Checked

Method: 2026-11-08 compared against the FileSystemShell page including its Object Storage section (apache/hadoop trunk markdown). Flags and behaviour match; the draft's `-ignorecrc` spelling is corrected to `-ignoreCrc`, missing flags added, `chmod` moved to no-op wording, and the invented "Verify" step removed.
