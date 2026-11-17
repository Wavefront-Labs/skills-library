---
id: computing-software.systems-network-administration.zfs.zpool-replace-device
name: zpool-replace-device
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, replace, resilver, failed-disk, sequential]
level: practitioner
status: docs-checked
description: "Replace a failed or old disk in a ZFS pool with zpool replace, including same-path replacement, -s sequential resilver and -w waiting."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-replace.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replacing a device

```
zpool replace [-fsw] [-o property=value] pool device [new-device]
```

It is equivalent to attaching `new-device`, waiting for it to resilver, then detaching `device`. A running scrub is cancelled.

```
zpool replace tank sda sdf          # different disk
zpool replace tank sda              # new disk in the same slot
```

If `new-device` is omitted it defaults to `device`, which suits a failed disk swapped for a new one at the same path. It is required if the pool is not redundant. The new device must be at least as large as the smallest device in a mirror or raidz.

## Flags

- `-f`: force `new-device` even if it appears in use.
- `-o ashift=...`: the only supported property.
- `-s`: sequential reconstruction, which restores redundancy faster. Checksums are not verified during it, and a scrub starts automatically when the resilver completes. Not supported for raidz.
- `-w`: block until the replacement finishes.

## Procedure

1. `zpool status -x` to identify the failed vdev.
2. Replace the device.
3. `zpool status` to monitor; `zpool wait -t replace tank` to script.

GUIDs from `zpool status -g` can be used in place of device names.

## Checked

2026-11-03. Pages read: zpool-replace(8), zpool-wait(8).

Confirmed: synopsis, equivalence to attach, resilver and detach, scrub cancellation, default new-device, size rule, -f, -o ashift, -s (not supported for raidz), -w.

Removed or corrected: the keep-attached advice and the zpool clear step, which the page does not give.

Method: documentation only; no commands were run.
