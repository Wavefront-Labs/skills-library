---
id: computing-software.systems-network-administration.virtualisation.proxmox-lvm-thin-storage
name: proxmox-lvm-thin-storage
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [lvm-thin, pve-lvm, thin-pool, pve-storage, storage-cfg, metadata-pool, lvextend, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Run LVM-thin storage on Proxmox VE: create and add a thin pool, watch data and metadata usage, extend pools, the full-pool failure mode, and LVM vs LVM-thin differences."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#storage_lvmthin
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#chapter_storage
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-lvmthin.adoc
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-lvm.adoc
  - https://github.com/proxmox/pve-docs/blob/master/pvesm.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LVM-thin storage on Proxmox VE

**Goal:** fast local block storage with snapshots and thin provisioning, monitored so the
pool never fills.

## LVM vs LVM-thin
| | LVM | LVM-thin |
|---|---|---|
| Provisioning | Thick | Thin |
| Snapshots | Only as volume chains (PVE 9, technology preview) | Yes |
| Shared across nodes | Possible on shared block storage (such as a SAN LUN) | No (local only) |
| Linked clones | No | Yes |

Regular LVM snapshots degrade write performance for the whole volume group, which is why PVE added snapshots as volume chains for LVM.

## Create and add a pool
```sh
lvcreate -L 100G -n data vmdata
lvconvert --type thin-pool vmdata/data
pvesm scan lvmthin vmdata                         # list thin pools in VG vmdata
pvesm add lvmthin vmdata-thin --vgname vmdata --thinpool data --content images,rootdir
```
The first two commands are the guide's example for creating a thin pool called `data` in an existing volume group `pve`. The storage entry takes `vgname` (an existing volume group) and `thinpool`. New volumes are initialised with zero. Volume names follow `vm-<VMID>-<NAME>`.

## Monitor
```sh
lvs -a vmdata
pvesm status
```
`lvs -a` also lists the hidden data and metadata volumes of the pool. Watch data and metadata usage yourself and choose alert thresholds for your environment. If a thin storage runs full, all guests on it receive I/O errors, which can corrupt file systems; avoid over-provisioning.

## Extend
Grow the pool and its metadata with the standard LVM tools (`vgextend`, `lvextend`; see `lvmthin(7)`), and use LVM's thin-pool auto-extend settings in `lvm.conf` only after reading its documentation.

## Gotchas
- Guest TRIM (`discard=on` on the VM disk plus a TRIM-capable guest OS) lets the storage release unused blocks; without it a thin pool only grows.
- Snapshots on a thin pool consume space as the guest writes; delete them after use.
- The default installer layout creates `local-lvm` (thin pool `data` in VG `pve`) on the boot disk, so heavy VM I/O shares that disk with the OS.

## Verify
`lvs` shows data and metadata below thresholds; a test write after `fstrim` in a guest
lowers `data_percent`; monitoring has an alert for both percentages.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09).

Confirmed: thin pool creation commands, `vgname` and `thinpool` properties, zero-initialised volumes, local-only (not shareable) use, snapshots and clones supported, `pvesm scan lvmthin`, default `local-lvm` entry and the full-storage I/O error warning; LVM (thick) snapshot situation (volume chains since PVE 9, technology preview, no linked clones, shared use possible); `discard` handling in the qm guide. Removed as unconfirmed: the 80% and 70% alert thresholds, the `lvm.conf` auto-extend values, the `lvextend` pool commands and the `-l 95%FREE` sizing.

Method: documentation only; no commands were run.
