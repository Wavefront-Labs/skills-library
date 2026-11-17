---
id: computing-software.systems-network-administration.virtualisation.proxmox-vm-snapshots-with-ram
name: proxmox-vm-snapshots-with-ram
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [qm-snapshot, qm, proxmox-vm, snapshots, vmstate, proxmox]
level: practitioner
status: docs-checked
description: "Use Proxmox VM snapshots well: which storages support them, including RAM (vmstate), rollback behaviour, snapshot trees, and why snapshots are not backups."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
  - https://pve.proxmox.com/pve-docs/chapter-pvesm.html
  - https://pve.proxmox.com/pve-docs/qm.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox VM snapshots (with RAM state)

## Storage support
| Storage | Snapshots |
|---|---|
| ZFS, Ceph RBD, LVM-thin, BTRFS (technology preview) | yes |
| Directory/NFS/CIFS with **qcow2** | yes (internal qcow2 snapshots, or snapshots as a volume chain) |
| LVM, iSCSI, FC/SAS | only with `snapshot-as-volume-chain` (Proxmox VE 9, technology preview; needs thin provisioning and discard on the backing storage for efficiency) |
Check the Snapshots column of the storage table in the storage chapter for your storage type. Creating and deleting internal qcow2 snapshots blocks a running VM and can take minutes, or hours for very large disks, especially on NFS; do it with the VM shut down if affected.

## Commands
```sh
qm snapshot 101 pre-upgrade --description "before app 4.2" --vmstate 1
qm listsnapshot 101
qm rollback 101 pre-upgrade          # VM stops; with vmstate it resumes at the saved moment
qm delsnapshot 101 pre-upgrade
```
`--vmstate 1` saves the VM memory. The target storage is the first of: the VM's `vmstatestorage`, the first shared storage of any VM disk, the first non-shared storage of any VM disk, then `local`. `qm rollback` has a `--start` option to start the VM afterwards.

## Behaviour to know
- With the QEMU guest agent enabled, taking a snapshot without RAM of a running VM issues a filesystem freeze first; without the agent the snapshot is not coordinated with the guest.
- Snapshot data is stored as a section in the VM configuration (`parent` and `snaptime` properties track the tree).
- Rollback discards everything after the snapshot, including data the app wrote; tell app owners.
- Memory-related features (snapshots with RAM, live migration, hibernate) are not available with virtiofs devices, and snapshots with RAM are not supported for memory-encrypted (AMD SEV) VMs.
- A snapshot with RAM is tied to the VM machine version; the machine version of a snapshot cannot be changed.

## Hygiene
Snapshots consume space as the VM diverges and can slow some storages. Keep them short-lived: delete (`qm delsnapshot`) after the change is accepted, and review `qm listsnapshot <vmid>` for each VM periodically.

## Not a backup
Snapshots live on the same storage; losing the pool loses them. Use vzdump/PBS for backups.

## Verify
After creating, `qm listsnapshot` shows the snapshot; a lab rollback returns the VM to the expected state; old snapshots are reviewed on a schedule.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: pvesm.adoc storage table and footnotes, pve-storage-lvm.adoc snapshot-as-volume-chain, qm.adoc Snapshots, State storage selection, QEMU Guest Agent freeze list and virtiofs and SEV limitations, generated qm.1-synopsis.adoc snapshot and rollback) and confirmed the snapshot support matrix, the volume-chain technology preview, the vmstate target-storage order, the qm snapshot, rollback --start and delsnapshot options, and the freeze behaviour. Removed the unconfirmed ZFS latest-only rollback, qcow2 tree, PCI passthrough, state volume naming and awk loop claims.

Method: documentation only; no commands were run.
