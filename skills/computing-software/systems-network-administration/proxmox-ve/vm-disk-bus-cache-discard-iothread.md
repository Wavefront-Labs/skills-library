---
id: computing-software.systems-network-administration.proxmox-ve.vm-disk-bus-cache-discard-iothread
name: vm-disk-bus-cache-discard-iothread
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [disk, virtio-scsi-single, iothread, discard, cache-mode]
level: practitioner
status: docs-checked
description: "Choose disk bus, image format, cache mode, discard and IO thread settings for Proxmox VE virtual machine disks."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prefer the VirtIO SCSI or VirtIO Block controllers: they perform best and are better maintained. IDE (4 devices) suits OSes older than 2003, SATA allows 6, SCSI 14. For performance use the controller type VirtIO SCSI single with the IO Thread setting on the disks; this is the default for new Linux VMs since 7.3 and gives each disk its own controller and a dedicated QEMU IO thread, which also reduces guest hangs under heavy host IO. IO thread works only with SCSI on VirtIO SCSI single or with VirtIO Block.

Image format follows the storage. Block-based storage (LVM, ZFS, Ceph) needs raw; file-based storage (ext4, XFS, NFS, CIFS) allows raw or qcow2. Qcow2 gives snapshots and thin provisioning; raw can be up to 10% faster but needs the storage layer for those features.

Cache mode: the default "No cache" reports a write complete when the block reaches the physical storage write queue, bypassing the host page cache, a good balance of safety and speed.

Discard: on thin-provisioned storage set Discard on the drive so TRIM from a TRIM-aware guest shrinks the image. Discard on VirtIO Block needs a guest kernel of 5.0 or newer, and SSD emulation is not supported on VirtIO Block.

Per-disk flags: "No backup" makes vzdump skip the disk, and "Skip replication" excludes it from replication. Replication needs disks on `zfspool` storage, so extra disks elsewhere must skip replication.

## Checked

2026-11-09. Compared with the Hard Disk section (bus, image format, cache, discard, IO thread, replication) of https://pve.proxmox.com/pve-docs/chapter-qm.html; controller limits, the 7.3 default, the 10% raw figure and the discard kernel version match.

Method: documentation only; no commands were run.

