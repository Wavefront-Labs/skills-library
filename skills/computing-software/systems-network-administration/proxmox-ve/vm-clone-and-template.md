---
id: computing-software.systems-network-administration.proxmox-ve.vm-clone-and-template
name: vm-clone-and-template
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [clone, template, linked-clone, full-clone, qm-template]
level: practitioner
status: docs-checked
description: "Convert VMs to templates and create linked or full clones with qm clone in Proxmox VE."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
  - https://pve.proxmox.com/pve-docs/qm.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```
qm template 9000
qm clone 9000 123 --name web1
qm clone 9000 124 --name db1 --full 1 --storage other-store
qm clone 100 125 --snapname snap1 --full
```

A full clone is an independent VM sharing no storage with the original. It can target another storage (`--storage`) and change the disk format (`--format qcow2|raw|vmdk`, full clone only), but must copy all data, so it is slower. It can clone a specific snapshot on storages that support it, never including the original's other snapshots.

A linked clone is a copy-on-write writable copy that is created almost instantly and initially uses no extra space. It still refers to the original, so the original must be read-only: convert the VM to a template. You cannot delete a template while linked clones exist, and you cannot change the target storage of a linked clone. By default, cloning a template tries a linked clone, while cloning a normal VM always makes a full copy.

Templates cannot be started because that would modify their disks. To change one, linked-clone it, modify the clone, and make it a template again.

Cloning randomises all NIC MAC addresses and generates a new `smbios1` UUID to avoid conflicts. `--target` creates the clone on another node, only allowed if the VM is on shared storage that the target also sees. `--bwlimit` caps copy IO in KiB/s. A `vmgenid` is generated for new VMs, and can be added with `qm set VMID -vmgenid 1`.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-qm.html, https://pve.proxmox.com/pve-docs/qm.1.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
