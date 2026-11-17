---
id: computing-software.systems-network-administration.zfs.zpool-initialize
name: zpool-initialize
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, initialize, uninit, suspend, cancel, new-disks]
level: practitioner
status: docs-checked
description: "Pre-write unallocated regions of ZFS leaf devices with zpool initialize, and cancel, suspend, resume, uninitialize or wait for it."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-initialize.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool initialize

```
zpool initialize [-c|-s|-u] [-w] [-z] -a|pool [device]...
```

With none of `-c`, `-s` or `-u`, it begins initializing: it writes to the unallocated regions of the named devices, or all eligible devices if none are named. Only leaf data or log devices can be initialized.

```
zpool initialize tank
zpool initialize tank sda sdb
zpool initialize -w tank
```

## Controls

- `-a` (`--all`): apply to all pools.
- `-s` (`--suspend`): suspend; run `zpool initialize` with no flags on the same devices to resume.
- `-c` (`--cancel`): cancel on the named or all eligible devices.
- `-u` (`--uninit`): clear the initialization state. Fails if a device is actively initializing. Afterwards a plain `zpool initialize` re-initializes all unallocated regions.
- `-w`: block until initialization finishes.
- `-z` (`--zero`): write zeroes instead of the default non-zero pattern. Useful for reclaiming space on thinly provisioned storage without TRIM; where TRIM is supported, zpool-trim is typically more efficient.

For `-c` and `-s`, if any target is invalid or not currently initializing, the command fails and changes nothing. The synopsis groups `-c|-s|-u` as alternatives.

## Monitoring

`zpool status -i tank` shows initialization status (see zpool-status-health). Script around it with:

```
zpool wait -t initialize tank
```

See zpool-wait.

## Checked

2026-11-03. Pages read: zpool-initialize(8).

Confirmed: synopsis, leaf data or log devices only, -a, -c, -s, -u, -w, -z, the all-or-nothing failure rule, and resume by running with no flags.

Removed or corrected: the missing -z option, now added.

Method: documentation only; no commands were run.
