---
id: computing-software.systems-network-administration.proxmox-ve.zfs-raid-level-selection
name: zfs-raid-level-selection
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [raid-level, volblocksize, raidz-padding, zvol, draid]
level: advanced
status: docs-checked
description: "Choose between mirror, RAIDZ and dRAID for VM workloads on Proxmox VE, and avoid RAIDZ zvol space amplification."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A pool is striped (RAID0) across its vdevs. For running VMs, IOPS is usually the more important metric.

- Mirror vdev: writes behave like one disk, reads scale with the number of disks. Four disks as two mirrors give the write IOPS of two disks and the read performance of four, with 50% usable space.
- RAIDZ at any level: IOPS of roughly one disk with high bandwidth. For four disks, two mirrors usually beat RAIDZ2 because usable space is the same.
- dRAID: performance similar to equivalent RAIDZ, spares take part in the RAID for faster rebuilds. It is intended for more than 10 to 15 disks. Defaults are 0 spares and 8 data devices per group; fewer data devices give higher IOPS and faster resilvering but less capacity. 

RAIDZ and zvols: VM disks are zvols with a default block size of 8k. With ashift 12 (4k blocks), a RAIDZ2 write of one 8k block adds two 4k parity blocks, so 16k is consumed. Observe it with:

```
zfs get volsize,refreservation,used <pool>/vm-<vmid>-disk-X
```

Counter measures are a larger `volblocksize` (settable only at zvol creation; the default can be changed in the storage configuration), mirror vdevs instead of RAIDZ, or `ashift=9`, which can perform badly depending on the disks and cannot be changed later.

Recommendation from the docs: use mirrors (RAID1 or RAID10) for VM workloads unless your environment can accept RAIDZ characteristics.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-sysadmin.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
