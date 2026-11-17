---
id: computing-software.systems-network-administration.virtualisation.proxmox-shared-lvm-over-iscsi-fc
name: proxmox-shared-lvm-over-iscsi-fc
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [shared-lvm, pve-iscsi, iscsi, fibre-channel, multipath, san, pve-storage, snapshot-as-volume-chain, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Use a SAN with Proxmox VE: iSCSI or FC LUNs with multipath, a shared LVM volume group on top, snapshot limits, and the PVE 9 snapshot-as-volume-chain option."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#storage_open_iscsi
  - https://pve.proxmox.com/wiki/Multipath
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#storage_lvm
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-iscsi.adoc
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-lvm.adoc
  - https://github.com/proxmox/pve-docs/blob/master/pvesm.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shared LVM over iSCSI or Fibre Channel on Proxmox VE

**Goal:** use an existing SAN array as shared VM storage for live migration and HA, the
way migrating VMware shops usually need.

## Stack
LUN (iSCSI or FC/SAS, usually with multipath) -> LVM volume group marked **shared** -> one LV per VM disk.
The guide states that the LVM backend implements cluster-wide locking when the storage is marked as shared, and that with iSCSI, FC or SAS shared storage LVM is used to split the LUN into virtual disks; the Multipath guide in the Proxmox wiki explains the multipath setup.

## Steps
1. iSCSI: add the target as PVE storage with `content none` so LUNs are not used directly (recommended when LVM goes on top):
   `pvesm add iscsi san1 --portal <host[:port]> --target <iqn> --content none`
   FC/SAS block storage is handled by the host without a storage plugin: zone and present the LUN to all nodes.
2. Configure multipathing on every node by following the Proxmox Multipath wiki guide.
3. Create the volume group once, on one node, on the (multipath) device: `pvcreate <device>` then `vgcreate san-vg <device>`.
4. Add it as shared LVM storage: `pvesm add lvm san-lvm --vgname san-vg --shared 1 --content images,rootdir`
   (`pvesm scan lvm` lists volume groups.)

## Snapshots
Regular LVM snapshots hurt write performance of the whole volume group, and LVM has no linked clones. Since PVE 9, VM snapshots on LVM are available as **snapshot as volume chain** (`snapshot-as-volume-chain` storage option, qcow2 layered on LVs); it is a technology preview, applies only to volumes created after it is enabled, and works best when the backing storage supports thin provisioning and discard. Otherwise rely on backups or array-side snapshots.

## Gotchas
- Build the PV on the multipath device, not on a single path device, so LVM does not pin one path.
- Thin provisioning, if any, lives on the array; `snapshot-as-volume-chain` needs thin provisioning and discard on the backing storage.
- Check the multipath guide and your array vendor's documentation for path-failure and LUN-resize procedures.

## Verify
`multipath -ll` shows all paths active on every node; `pvs` shows the PV on
`/dev/mapper/...`; a VM on san-lvm live-migrates between nodes; pulling one path keeps I/O.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09).

Confirmed: iSCSI `content none` tip and `pvesm add iscsi --portal --target`; LVM on top of an iSCSI LUN or FC SAN; cluster-wide locking when `shared` is set; snapshot-as-volume-chain (PVE 9, technology preview, thin provisioning and discard needed for efficiency, LVM has no linked clones); `pvesm scan lvm`; FC/SAS handled without a plugin; footnote pointing to the Multipath wiki guide. Removed as unconfirmed (multipath-tools and udev specifics are outside the PVE docs): the `scsi_id`/`multipath -a`/`multipathd resize` commands, the LVM device-filter advice, the "do not use lvmlockd" statement and the discard advice for arrays.

Method: documentation only; no commands were run.
