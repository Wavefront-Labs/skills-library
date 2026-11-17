---
id: computing-software.systems-network-administration.proxmox-ve.vm-disk-move-resize-import
name: vm-disk-move-resize-import
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [qm-disk-move, qm-disk-resize, import-from, move-disk, qm-importdisk]
level: practitioner
status: docs-checked
description: "Move, resize, reassign and import disks of Proxmox VE virtual machines with qm disk commands."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
  - https://pve.proxmox.com/pve-docs/qm.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Move a disk to another storage, optionally changing format; by default the old disk is kept as an unused disk unless you pass `--delete 1`:

```
qm disk move 300 scsi0 other-storage
qm move-disk 300 scsi0 other-storage --format qcow2 --delete 1
qm move-disk 300 scsi1 --target-vmid 400 --target-disk scsi3
```

The last form reassigns the disk to another VM (renaming the image to match the new owner). Format changes apply only when moving between storages, and unsupported formats fall back to the storage default. Both `--bwlimit` (KiB/s) and `--digest` (reject if the config changed concurrently) exist.

Grow a disk; shrinking is not supported:

```
qm disk resize 300 scsi0 +10G
qm disk resize 300 scsi0 50G
```

A leading `+` adds to the current size, otherwise the value is absolute. The guest filesystem must be grown inside the guest afterwards.

Import an external image, for example from another hypervisor or a cloud image, directly at creation or later:

```
qm create 600 --net0 virtio,bridge=vmbr0 --name vm600 --scsihw virtio-scsi-pci \
  --boot order=scsi0 --scsi0 pvedir:0,import-from=/path/to/dir/vm600.raw
qm set 9000 --scsi0 local-lvm:0,import-from=/path/to/cloudimg.img
```

The `0` size means take the size from the source. `qm disk import` is the CLI for an existing VM. An unused disk can be attached again from the VM hardware panel, or removed with `qm disk unlink`. Rescan with `qm disk rescan` after changing volumes outside Proxmox.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-qm.html, https://pve.proxmox.com/pve-docs/qm.1.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
