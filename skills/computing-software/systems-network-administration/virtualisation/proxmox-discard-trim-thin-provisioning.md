---
id: computing-software.systems-network-administration.virtualisation.proxmox-discard-trim-thin-provisioning
name: proxmox-discard-trim-thin-provisioning
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-discard, fstrim-guest, pve-storage, lvm-thin, thin-provisioning, qemu-guest-agent, proxmox]
level: practitioner
status: docs-checked
description: "Reclaim thin-provisioned space on Proxmox: discard=on and SSD emulation on disks, guest fstrim, agent fstrim after migration, and checking LVM-thin, ZFS and Ceph usage."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
  - https://github.com/proxmox/pve-docs/blob/master/qm.adoc
  - https://github.com/proxmox/pve-docs/blob/master/pvesm.adoc
  - https://github.com/proxmox/qemu-server/blob/master/src/PVE/API2/Qemu/Agent.pm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Discard/TRIM and thin provisioning on Proxmox VE

Thin storages (LVM-thin, ZFS zvols, Ceph RBD, qcow2) only shrink when the guest tells
them which blocks are free. Without discard, usage only grows until the pool fills and
a full storage gives **every guest on it I/O errors**, which can corrupt file systems.

## Enable on the virtual disk
```sh
qm set 101 --scsi0 local-lvm:vm-101-disk-0,discard=on,ssd=1,iothread=1
```
- With **Discard** set and a TRIM-capable guest OS, when the guest file system marks blocks unused the controller relays that to the storage, which shrinks the disk image. The storage must support thin provisioning.
- **Discard** on VirtIO Block drives is supported only on guests running Linux kernel 5.0 or newer; some guest operating systems also need the **SSD emulation** flag (`ssd=1`) to issue TRIM. SSD emulation is not supported on VirtIO Block drives. SSD emulation only changes how the drive is presented; the storage need not be SSD.

## In the guest
Run TRIM inside the guest with its own tools (for Linux, `fstrim`; see the distribution's documentation for scheduling), using the guest OS documentation rather than this skill.

## From the host via the guest agent
Enable *Run guest-trim* (QEMU Guest Agent option): PVE then issues a trim command to the guest after moving a disk to another storage and after live-migrating a VM to a node with local storage. On demand, from the host:
```sh
qm guest cmd 101 fstrim
```
Caveat from the guide: for ext4 on Linux only the first guest-trim after a reboot behaves as expected, because subsequent ones consider only newly freed blocks.

## Check the result
Use the storage's own tools: `lvs -a` (Data% of thin volumes and the pool) for LVM-thin, `zfs list -o name,used,refer,volsize <dataset>` for ZFS, `rbd du` for Ceph RBD. Watch free space yourself: when a storage runs full, all guests on it get I/O errors, which can corrupt file systems.

## Gotchas
- Snapshots keep their blocks until deleted, so trim reduces usage little while old snapshots exist.
- Thin provisioning means volumes can be larger than the free space: avoid over-provisioning.

## Verify
After `qm guest cmd 101 fstrim`, thin usage drops toward guest-used size; pool Data%
trends stable rather than monotonic growth.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and qemu-server source (guest agent `fstrim` command).

Confirmed: Trim/Discard behaviour, VirtIO Block kernel 5.0 requirement, SSD emulation notes, the *Run guest-trim* option and its triggers, the ext4 caveat, `qm guest cmd <vmid> fstrim` (the agent command list includes `fstrim`), the full-storage I/O error warning. Removed as unconfirmed: IDE/SATA wording, 'ssd=1 enables periodic trim in Windows', stop/start requirement, Linux `fstrim.timer` and Windows `fsutil` details, the 80% alert, the `refreservation` remark and the `lvextend --poolmetadatasize` advice.

Method: documentation only; no commands were run.
