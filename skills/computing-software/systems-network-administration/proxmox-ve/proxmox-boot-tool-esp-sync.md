---
id: computing-software.systems-network-administration.proxmox-ve.proxmox-boot-tool-esp-sync
name: proxmox-boot-tool-esp-sync
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [proxmox-boot-tool, esp, systemd-boot, grub, efibootmgr]
level: advanced
status: docs-checked
description: "Keep EFI System Partitions in sync with proxmox-boot-tool and identify which bootloader a host uses."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Proxmox VE uses systemd-boot for EFI installs with ZFS root when Secure Boot is off, and GRUB for everything else. The installer creates a 1 MB BIOS boot partition, a 512 MB ESP and a data partition on each selected disk. `proxmox-boot-tool` copies kernels and initrds to every listed ESP and configures the bootloader on them. The ESPs are deliberately not mounted during normal operation, to avoid vfat corruption after a crash.

```
proxmox-boot-tool status
proxmox-boot-tool format /dev/sda2
proxmox-boot-tool init /dev/sda2
proxmox-boot-tool init /dev/sda2 grub
proxmox-boot-tool refresh
```

`format` wipes the partition, so check the device. `init` adds the ESP UUID to `/etc/kernel/proxmox-boot-uuids`; pass `grub` to force GRUB, which Secure Boot needs. `refresh` (equivalent to `update-grub` on ext4/xfs roots) is needed after kernel command line changes; apt and `update-initramfs` trigger it automatically.

Default kernels kept in sync: the running kernel, the newly installed one, the two latest installed, and manually added ones (`proxmox-boot-tool kernel add|remove|list VERSION`).

To tell the bootloader apart run `efibootmgr -v`. A `grubx64.efi` entry means GRUB in UEFI mode, `shimx64.efi` means GRUB with Secure Boot, `systemd-bootx64.efi` means systemd-boot, and an "EFI variables are not supported" message means legacy BIOS GRUB.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-sysadmin.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
