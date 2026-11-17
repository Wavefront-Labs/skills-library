---
id: computing-software.systems-network-administration.zfs.zpool-attach-mirror
name: zpool-attach-mirror
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, attach, mirror, resilver, sequential]
level: practitioner
status: docs-checked
description: "Turn a single disk into a mirror or widen a mirror with zpool attach, use sequential resilver -s and wait with -w."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-attach.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attaching to a mirror

```
zpool attach [-fsw] [-o property=value] pool vdev new_device
```

`vdev` is an existing plain device or mirror (e.g. `sda`, `mirror-7`); `new_device` is the disk to add.

```
zpool attach tank sda sdb
```

A plain device becomes a two-way mirror. Attaching to an existing mirror makes a three-way mirror, and so on.

## Behaviour

- Resilver starts immediately and any running scrub is cancelled.
- `new_device` adds redundancy once the resilver completes.

## Flags

- `-f`: force a `new_device` that appears in use.
- `-o ashift=...`: the only supported property.
- `-s`: reconstruct sequentially (mirror or plain vdevs only). Redundancy returns faster, but checksums are not verified during reconstruction, so a scrub starts when the resilver finishes.
- `-w`: block until the resilver finishes.

## Check progress

```
zpool status tank
zpool wait -t resilver tank
```

To detach a disk afterwards use `zpool detach`; a non-log mirror member is removed with `detach`, not `remove`. See also zpool-replace-device and zpool-split-pool.

## Checked

2026-11-03. Pages read: zpool-attach(8), zpool-remove(8).

Confirmed: synopsis, mirror and plain-device behaviour, three-way mirrors, resilver starting and scrub cancellation, -f, -o ashift, -s (checksums not verified, scrub follows), -w, and that mirror members are removed with detach.

Removed or corrected: the size requirement, which the page states only for RAID-Z expansion.

Method: documentation only; no commands were run.
