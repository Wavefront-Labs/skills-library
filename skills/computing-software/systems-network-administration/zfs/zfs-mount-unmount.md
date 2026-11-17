---
id: computing-software.systems-network-administration.zfs.zfs-mount-unmount
name: zfs-mount-unmount
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, mount, unmount, mountpoint, overlay, legacy]
level: intro
status: docs-checked
description: "Mount and unmount ZFS filesystems with zfs mount and unmount, including -a, -R, -O overlay, -o options, -l key loading and forced unmounts."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-mount.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mounting

```
zfs mount [-j]
zfs mount [-Oflv] [-o options] -a|-R filesystem|filesystem
zfs unmount [-fu] -a|filesystem|mountpoint
```

`zfs mount` alone lists mounted ZFS filesystems (`-j` for JSON).

A filesystem mounts at its `mountpoint` property path, which must exist and be empty unless you use `-O`. Datasets with `mountpoint=legacy` are mounted with `mount(8)` instead.

## Mount flags

- `-a`: all available filesystems (done automatically at boot when configured)
- `-R`: the named filesystem and all children
- `-O`: overlay mount, allowing a non-empty mountpoint
- `-o options`: comma-separated mount options for this mount only
- `-l`: load keys for encrypted filesystems first; a `prompt` keylocation blocks at the terminal
- `-v`: report progress
- `-f`: try to force-mount filesystems that normally cannot be mounted, such as redacted datasets

## Unmount flags

- `-a`: all
- `-f`: force even if in use (not supported on Linux)
- `-u`: unload keys of encryption roots unmounted by this command

```
zfs unmount tank/data
zfs unmount /mnt/data
zfs mount -R tank/projects
```

## Checked

2026-11-03. Confirmed against zfs-mount(8): synopsis, `-j`, `-O`, `-a`, `-R`, `-o`, `-l`, `-v`, `-f`, unmount `-a`/`-f`/`-u`, legacy mountpoints. Removed the unsupported busy-mountpoint advice.
Method: documentation only; no commands were run.
