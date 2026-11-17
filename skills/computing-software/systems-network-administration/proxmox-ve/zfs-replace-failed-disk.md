---
id: computing-software.systems-network-administration.proxmox-ve.zfs-replace-failed-disk
name: zfs-replace-failed-disk
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [zpool-replace, resilver, sgdisk, boot-disk, failed-disk]
level: advanced
status: docs-checked
description: "Replace a failed ZFS disk on a Proxmox VE host, including the extra steps for a bootable rpool disk."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For a non-boot data disk the replacement is one command, then watch the resilver:

```
zpool replace -f <pool> <old-device> <new-device>
zpool status -v
```

For a failed disk of the boot pool, also recreate the partition layout and make the new disk bootable. First find the bootloader setup with `proxmox-boot-tool status`. Then copy the partition table from a healthy bootable disk, give the new disk fresh GUIDs, and replace the ZFS partition (the third partition, not the whole disk):

```
sgdisk <healthy bootable device> -R <new device>
sgdisk -G <new device>
zpool replace -f <pool> <old zfs partition> <new zfs partition>
```

Order the arguments carefully: `-R` replicates the table from the device given first onto the new device, so a swapped argument would overwrite the healthy disk.

Make it bootable:

- With proxmox-boot-tool (systems installed with Proxmox VE 6.4 or later, or EFI systems from 5.4 or later): `proxmox-boot-tool format <new disk's ESP>` then `proxmox-boot-tool init <new disk's ESP> [grub]`. The ESP is partition 2 on installer-created disks. Pass `grub` when `status` shows GRUB, especially with Secure Boot.
- Plain GRUB (installs from 6.3 or earlier not yet migrated): `grub-install <new disk>`.

Monitor progress with `zpool status -v` until resilvering completes.

## Checked

2026-11-09. Compared with the Changing a failed device and Changing a failed bootable device sections of https://pve.proxmox.com/pve-docs/chapter-sysadmin.html; commands, bootloader version notes and the ESP partition note match.

Method: documentation only; no commands were run.

