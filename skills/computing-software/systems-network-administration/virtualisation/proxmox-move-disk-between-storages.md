---
id: computing-software.systems-network-administration.virtualisation.proxmox-move-disk-between-storages
name: proxmox-move-disk-between-storages
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [qm-move-disk, disk-move, pve-storage, pct-move-volume, live-storage-migration, proxmox]
level: practitioner
status: docs-checked
description: "Move VM disks and container volumes between Proxmox storages online with qm disk move and pct move-volume, format conversion, bandwidth limits and cleanup."
sources:
  - https://pve.proxmox.com/pve-docs/qm.1.html
  - https://pve.proxmox.com/pve-docs/pct.1.html
  - https://github.com/proxmox/pve-docs/blob/master/qm.adoc
  - https://github.com/proxmox/pve-docs/blob/master/pct.adoc
  - https://github.com/proxmox/pve-docs/blob/master/pvesm.adoc
  - https://github.com/proxmox/qemu-server/blob/master/src/PVE/API2/Qemu.pm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Moving disks between storages

## VMs
```sh
qm move-disk 101 scsi0 ceph-vm --delete 1            # move and remove the source
qm move-disk 101 scsi1 local-zfs --format raw        # format applies to the target storage (raw, qcow2, vmdk)
qm move-disk 101 scsi0 nfs-store --format qcow2 --bwlimit 204800   # KiB/s
```
`qm move-disk` is the documented name. `--format` is used only when moving to a different storage; if the target does not support it, the storage's default format is used. `--delete` removes the original disk after a successful copy; without it the old volume stays as an `unused` disk of the VM and keeps consuming space. `--bwlimit` overrides the I/O bandwidth limit in KiB/s. The caller needs `VM.Config.Disk` on the VM. If the *Run guest-trim* guest agent option is enabled, PVE issues a trim to the guest after moving a disk to another storage.

## Containers
```sh
pct move-volume 201 mp0 other-storage
pct move-volume 201 rootfs local-zfs --delete 1
```
`pct move-volume` moves a container mount point volume (or the root volume) to a different storage; check `pct help move-volume` on your release for the `--delete` and online-move behaviour.

## Moving to another VM (reassign)
`qm move-disk 101 scsi1 --target-vmid 102 --target-disk scsi3` removes the disk from the source VM and attaches it to the target VM; the disk image is renamed to match the new owner. For containers: `pct move-volume 100 mp0 --target-vmid 200 --target-volume mp1`.

## Formats and storage types
| Target storage type | Image formats (storage tables) |
|---|---|
| ZFS pool | raw, subvol |
| LVM-thin | raw |
| LVM | raw (qcow2 since PVE 9 for snapshots as volume chains) |
| Directory, NFS, CIFS | raw, qcow2, vmdk |
| Ceph RBD | raw |
Snapshots on file-based storages need `qcow2`.

## Gotchas
- Snapshots: file storages implement snapshots with `qcow2`; check the storage feature tables before moving a VM that has snapshots to a different storage type.
- Replication jobs (pvesr) work only for ZFS volumes; moving a disk off ZFS removes that guest's ability to replicate.
- Disks that use the same storage ID after a move keep their volume ID rules (`<storage>:<volume>`).

## Verify
`qm config 101` shows the disk on the new storage, no `unusedN` entries left if deleted,
`pvesm list <old-storage> --vmid 101` empty.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and qemu-server source (`move_vm_disk` API).

Confirmed: `qm move-disk` usage including `--target-vmid` and `--target-disk` reassign semantics, `pct move-volume` usage and its reassign example; API parameters `format` (raw, qcow2, vmdk; only for a different storage; falls back to the storage default), `delete`, `bwlimit` (KiB/s), `VM.Config.Disk` permission; guest-trim after disk move; storage feature tables for the format list. Changed: `qm disk move` replaced by the documented `qm move-disk`. Removed as unconfirmed: the QEMU drive-mirror remark, 'container must be stopped', the GUI path, the thin-keeping qcow2 to raw claim, the live-convergence advice and the cloud-init remark.

Method: documentation only; no commands were run.
