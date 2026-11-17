---
id: computing-software.systems-network-administration.zfs.zpool-destroy-pool
name: zpool-destroy-pool
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, destroy, decommission, destroyed-pools]
level: intro
status: docs-checked
description: "Destroy a ZFS pool with zpool destroy, what -f does to mounted datasets, releasing devices, and listing destroyed pools with zpool import -D."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-destroy.8.html
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-import.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool destroy

```
zpool destroy [-f] pool
```

Destroys the named pool and every dataset in it, releasing its devices for other uses. It first attempts to unmount active datasets.

```
zpool destroy tank
zpool destroy -f tank
```

`-f` forcefully unmounts all active datasets before destroying. Without it, unmounts are not forced.

This is the only documented option.

## Before you run it

1. Name the pool exactly; confirm with `zpool list`.
2. If you only want to move disks to another host, use zpool-export-pool instead, not destroy.

## Destroyed pools can be found

Destroyed pools are hidden from normal listings. `zpool import -D` lists only destroyed pools, and importing one needs `-D` plus `-f`:

```
zpool import -D
zpool import -D -f tank
```

With `-a`, destroyed pools are imported only when `-D` is given.

## Checked

2026-11-03. Pages read: zpool-destroy(8), zpool-import(8).

Confirmed: synopsis, -f, unmounting behaviour, freeing of devices, import -D for listing and importing destroyed pools with -f.

Removed or corrected: the copy-first step and the safety-net remark, which the pages do not give.

Method: documentation only; no commands were run.
