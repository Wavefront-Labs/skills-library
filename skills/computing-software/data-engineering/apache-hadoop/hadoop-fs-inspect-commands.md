---
id: computing-software.data-engineering.apache-hadoop.hadoop-fs-inspect-commands
name: hadoop-fs-inspect-commands
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, fs-shell, count, stat, test, find, ls, expunge]
level: intro
status: docs-checked
description: "Inspecting HDFS from the shell: count flags, stat format specifiers, test options, find primaries, ls sorting flags, expunge, tail and touch."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/FileSystemShell.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fs shell: inspection

- count: `hadoop fs -count [-q] [-h] [-v] [-x] [-t [type]] [-u] [-e] [-s] <paths>`. Default columns DIR_COUNT, FILE_COUNT, CONTENT_SIZE, PATHNAME. `-q` adds quotas and usage; `-u` limits output to quotas only; `-t` per storage type (all, ram_disk, ssd, disk, archive) and is ignored without `-u` or `-q`; `-h` human sizes; `-v` header; `-x` excludes snapshots (default includes them; ignored with `-u`/`-q`); `-e` shows the erasure coding policy ("Replicated" if none); `-s` snapshot counts.
- ls: `hadoop fs -ls [-C] [-d] [-h] [-q] [-R] [-t] [-S] [-r] [-u] [-e] <args>`. `-C` paths only, `-d` directories as plain files, `-q` print ? for non-printable characters, `-t` modification time (most recent first), `-S` size, `-r` reverse, `-u` access time instead of modification time, `-e` erasure coding policy only. Default order is by filename.
- stat: `hadoop fs -stat [format] <path>`. Specifiers: `%a` octal permissions, `%A` symbolic, `%b` size in bytes, `%F` type, `%g` group, `%n` name, `%o` block size, `%r` replication, `%u` user, `%x`/`%X` access time, `%y`/`%Y` modification time. Lowercase x/y give UTC "yyyy-MM-dd HH:mm:ss"; uppercase give milliseconds since the epoch. Default format is `%y`.
- test: `hadoop fs -test -[defswrz] URI`. `-d` directory, `-e` exists, `-f` file, `-s` not empty, `-w` exists and writable, `-r` exists and readable, `-z` zero length; returns 0 when true.
- find: `hadoop fs -find <path> <expression>`. Defaults to the working directory and `-print`. Primaries include `-name`/`-iname`, `-regex`/`-iregex`, `-type` (d, l, f), `-size n[c]`, `-mtime`/`-mmin`, `-atime`/`-amin`, `-user`, `-group`, `-perm`, `-empty`, `-replicas`, `-blocksize`, `-newer`, `-print`/`-print0`. Only the AND operator exists (`-a`, `-and`, or juxtaposition). Escape wildcards so the shell does not expand them.
- head / tail: first / last kilobyte; `tail -f` follows appended data.
- touch: `-a` access time only, `-m` modification time only, `-t yyyyMMdd:HHmmss`, `-c` do not create a missing file.
- expunge: `hadoop fs -expunge [-immediate] [-fs path]` creates a new trash checkpoint and permanently deletes checkpoints older than `fs.trash.interval`; `-immediate` deletes all of the current user's trash regardless of the interval.
- `hadoop fs -usage <command>` and `-help` show help.

## Checked

Method: 2026-11-08 compared against the FileSystemShell page (apache/hadoop trunk markdown, read in full). Corrected the draft's `-u` description (quotas only, not "quotas and usage") and added defaults and unit details; removed the unsupported "Verify" step.
