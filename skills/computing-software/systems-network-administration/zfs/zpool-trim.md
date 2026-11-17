---
id: computing-software.systems-network-administration.zfs.zpool-trim
name: zpool-trim
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, trim, ssd, secure-trim, rate-limit, systemd-timer]
level: practitioner
status: docs-checked
description: "Run on-demand TRIM on ZFS pools with zpool trim: secure TRIM, rate limiting, suspend and resume, cancel, waiting, and periodic systemd timers."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-trim.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool trim

```
zpool trim [-dw] [-r rate] [-c|-s] -a|pool [device]...
```

Starts an immediate TRIM of all free space so thinly provisioned devices can reclaim it. It works regardless of the `autotrim` property. The man page defers the list of eligible vdev types to the autotrim property documentation.

```
zpool trim tank
zpool trim tank sda
zpool trim -w tank
```

## Options

- `-a`: all pools.
- `-d` (`--secure`): secure TRIM, where the device guarantees trimmed data is erased. The device must support it; not all SSDs do.
- `-r rate`: cap progress in bytes per second, per vdev; can be set per leaf vdev. Without it, TRIM runs as fast as possible.
- `-s` (`--suspend`): suspend trimming on the named devices or all eligible devices. Resume by running `zpool trim` without flags on them.
- `-c` (`--cancel`): cancel trimming. For both `-c` and `-s`, an invalid device or one not being trimmed makes the command fail and affect nothing.
- `-w`: block until trimming finishes.

## Periodic trim on systemd

```
systemctl enable --now zfs-trim-weekly@rpool.timer
```

Weekly and monthly timers exist per pool. For trim progress see `zpool status -t` (see zpool-status-health).

## Checked

2026-11-03. Pages read: zpool-trim(8).

Confirmed: synopsis, independence from autotrim, -a, -d, -r, -c, -s, -w, and the weekly and monthly systemd timer units.

Removed or corrected: the unsupported mention of flash devices.

Method: documentation only; no commands were run.
