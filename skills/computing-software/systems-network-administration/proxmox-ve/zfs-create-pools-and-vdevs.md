---
id: computing-software.systems-network-administration.proxmox-ve.zfs-create-pools-and-vdevs
name: zfs-create-pools-and-vdevs
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [zfs, zpool-create, ashift, raidz, mirror]
level: practitioner
status: docs-checked
description: "Create ZFS pools on Proxmox VE with zpool create, choosing ashift, mirror, RAIDZ, cache and log devices."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZFS needs direct disk access, so use an HBA (or a controller in IT mode), never a hardware RAID with its own cache. At least 8 GB of RAM is advised and ECC memory is recommended.

Create pools with `ashift` equal to or larger than the disk sector size (2^ashift):

```
zpool create -f -o ashift=12 <pool> <device>
zpool create -f -o ashift=12 <pool> mirror <dev1> <dev2>
zpool create -f -o ashift=12 <pool> mirror <dev1> <dev2> mirror <dev3> <dev4>
zpool create -f -o ashift=12 <pool> raidz1 <dev1> <dev2> <dev3>
zpool create -f -o ashift=12 <pool> raidz2 <dev1> <dev2> <dev3> <dev4>
zfs set compression=lz4 <pool>
```

Minimum disks: RAID0 1, RAID1 2, RAID10 4, RAIDZ-1 3, RAIDZ-2 4, RAIDZ-3 5. Pool names must start with a letter, may contain alphanumerics and `- _ . :` and space, must not begin with mirror, raidz, draid or spare, and must not be `log`.

Dedicated devices: `zpool create ... <device> cache <cache-device>` adds an L2ARC (cache devices are simply accumulated, with no mirror or RAID). `... <device> log <log-device>` adds a ZIL/SLOG for synchronous writes on fast SSDs with power-loss protection. If all log devices fail the main pool is used again. On an existing pool: `zpool add <pool> log <dev-part1> cache <dev-part2>` using `/dev/disk/by-id/` partition paths.

Proxmox VE 9 (ZFS 2.3.3) can extend a RAIDZ vdev with `zpool attach <pool> <raidzN-M> <device>`; check with `zpool status <pool>` and `zpool list <pool> -v`.

## Checked

2026-11-09. Confirmed against the Proxmox VE docs chapter Host System Administration (chapter-sysadmin), ZFS on Linux section: pool creation examples, ashift, pool name rules, L2ARC cache and ZIL log devices, log failure fallback, RAIDZ expansion with zpool attach on Proxmox VE 9 (ZFS 2.3.3).

Method: documentation only; no commands were run.
