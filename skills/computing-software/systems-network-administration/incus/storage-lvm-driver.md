---
id: computing-software.systems-network-administration.incus.storage-lvm-driver
name: storage-lvm-driver
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, storage, lvm, thin-pool, lvmcluster, lvmlockd, sanlock, volume-group]
level: advanced
status: docs-checked
description: "Run Incus on LVM: thin pools by default, lvm.use_thinpool and lvm.vg.force_reuse, retain settings, and the lvmcluster driver prerequisites with lvmlockd and sanlock."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/reference/storage_lvm.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LVM driver

- Images use logical volumes; instances and snapshots use volume snapshots. Pools use a thin pool by default.
- Incus assumes full control of the volume group and may delete foreign content. Reuse an existing group with `lvm.vg.force_reuse`.
- `lvm.use_thinpool=false` switches to normal volumes with serious performance and space penalties (no snapshots of snapshots; non-thin snapshots reserve full size).
- High-turnover setups such as CI should tune `retain_min` and `retain_days` in `/etc/lvm/lvm.conf`.

`lvmcluster` driver (shared block device such as FC, NVMe-oF or iSCSI LUN):
- Packages `lvm`, `lvmlockd`, `sanlock`; both daemons running.
- `use_lvmlockd = 1` in `/etc/lvm/lvm.conf`; a unique `host_id` per member in `/etc/lvm/lvmlocal.conf`.
- No thin provisioning, so usage is higher. No snapshots of shared custom volumes or raw block volumes; only `raw` custom volumes support `security.shared`.

## Checked

2026-11-04: confirmed against the Incus LVM storage driver reference page (thin pool default, `lvm.vg.force_reuse`, `lvm.use_thinpool=false` penalties, `retain_min`/`retain_days`, lvmcluster requirements and limitations). Nothing removed.

Method: documentation only; no commands were run.
