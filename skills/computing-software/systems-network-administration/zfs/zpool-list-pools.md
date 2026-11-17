---
id: computing-software.systems-network-administration.zfs.zpool-list-pools
name: zpool-list-pools
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, list, capacity, fragmentation, json]
level: intro
status: docs-checked
description: "List ZFS pools with zpool list: default columns, -v per-vdev usage, -o column selection, scripting mode, timestamps and JSON."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-list.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool list

```
zpool list [-HgLpPv] [-j [--json-int, --json-pool-key-guid]] [-o property[,property]...] [-T u|d] [pool]... [interval [count]]
```

With no pool names, all imported pools are listed.

Default columns: name, size, allocated, free, checkpoint, expandsize, fragmentation, capacity, dedupratio, health, altroot.

```
zpool list
zpool list -v tank
zpool list -Hp -o name,capacity,health
zpool list -j --json-int
```

## Flags

- `-v`: add per-vdev usage beneath the pool line.
- `-o`: choose columns using names from zpoolprops(7).
- `-H`: scripted mode, tab-separated, no header. `-p`: exact numbers.
- `-g`, `-L`, `-P`: GUIDs, resolved symlinks, full paths for vdev names.
- `-T u|d`: timestamps.
- `interval` and `count`: repeat reports.
- `-j`: JSON; `--json-int` for integers; `--json-pool-key-guid` keys pool objects by GUID.

## Reading it

- A pool that cannot be opened shows `-` for numeric fields and a state like FAULTED.
- `EXPANDSZ` is unused space on a device that has grown; the pool cannot use it until every device in the vdev is expanded (see `zpool online -e`).
- `checkpoint` shows space used by a checkpoint.

## Checked

2026-11-03. Pages read: zpool-list(8), zpool-checkpoint(8).

Confirmed: synopsis, default column list, -v, -o, -H, -p, -g, -L, -P, -T, interval and count, -j options, the `-` for a faulted pool and the expandsize behaviour from the examples.

Removed or corrected: the monitoring advice and the CKPOINT column name, which the page does not use.

Method: documentation only; no commands were run.
