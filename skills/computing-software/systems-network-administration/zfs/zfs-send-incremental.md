---
id: computing-software.systems-network-administration.zfs.zfs-send-incremental
name: zfs-send-incremental
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, send, incremental, replication, dry-run, progress]
level: practitioner
status: docs-checked
description: "Produce full and incremental ZFS send streams with -i and -I, preview with -nvP, and report progress with -v."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-send.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Basic and incremental sends

```
zfs send [-DLPUVcensvw] [-i snapshot|bookmark] filesystem|volume|snapshot
zfs send [-I|-i] snapshot snapshot
```

A full stream:

```
zfs send tank/data@a | ssh backup zfs receive pool/data
```

## Incremental

- `-i snapshot|bookmark`: send changes from the source to the target. The source may be a short `@name` if in the same filesystem, or a bookmark. If the target is a clone, the source may be its origin, written in full.
- `-I snapshot`: send all intermediate snapshots between the first and second. `-I @a fs@d` is like chaining `-i` through `@b` and `@c`.

```
zfs send -i @a tank/data@b | ssh backup zfs receive pool/data
zfs send -I @a tank/data@d | ssh backup zfs receive pool/data
```

## Preview and progress

- `-n` produces no stream; with `-v` or `-P` it reports what would be sent (to standard output rather than standard error).
- `-v` prints stream info and a per-second progress report to stderr; `SIGINFO` or `SIGUSR1` triggers a report regardless.
- `-P` makes output machine-parsable.
- `-V` sets the process title to a progress report.

The stream format is committed, so it is stable. Use `-h` to include snapshot holds, which the receiver applies.

## Checked

2026-11-03. Confirmed against zfs-send(8): `-i`, `-I`, `-n`, `-v`, `-P`, `-V`, `-h`, SIGINFO/SIGUSR1, the committed stream format and the synopsis flags. Fixed the synopsis flag list to match the man page and removed the unsupported claim that `-n` reports size.
Method: documentation only; no commands were run.
