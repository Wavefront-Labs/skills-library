---
id: computing-software.systems-network-administration.zfs.zfs-list-datasets
name: zfs-list-datasets
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, list, datasets, sorting, json, scripting]
level: intro
status: docs-checked
description: "List ZFS datasets, snapshots and bookmarks with zfs list: columns, sorting, depth, types, scripting mode and JSON output."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-list.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zfs list

```
zfs list [-r | -d depth] [-Hp] [-j [--json-int]] [-o property[,property]...] [-s property]... [-S property]... [-t type[,type]...] [dataset]...
```

Default columns are name, used, available, referenced and mountpoint. By default filesystems and volumes show; snapshots show only with the pool property `listsnapshots` on, or with `-t snapshot` or `-t all`.

## Common recipes

```
zfs list -r tank
zfs list -d 1 -o name,used,avail tank
zfs list -t snapshot -s creation -r tank/data
zfs list -o space
zfs list -Hp -o name,used -t filesystem
```

## Flags

- `-r` recurse into all children; `-d depth` limit recursion (`-d 1` is the dataset and direct children).
- `-o`: native or user properties, `name`, or `space` (shortcut for name, avail, used, usedsnap, usedds, usedrefreserv, usedchild).
- `-s` ascending and `-S` descending sort, repeatable; leftmost has priority.
- `-t`: `filesystem`, `snapshot`, `volume`, `bookmark` or `all` (aliases `fs`, `snap`, `vol`).
- `-H`: no header, tab-separated. `-p`: exact numbers.
- `-j` / `--json`: JSON; add `--json-int` for integer numbers.

Rows where a sort property does not apply sort to the bottom.

## Checked

2026-11-03. Confirmed against zfs-list(8): synopsis, default columns, `listsnapshots`, `-r`, `-d`, `-o` including `space`, `-s`/`-S`, `-t` types and aliases, `-H`, `-p`, `-j`/`--json-int`, and sort-to-bottom behaviour.
Method: documentation only; no commands were run.
