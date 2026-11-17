---
id: computing-software.systems-network-administration.proxmox-ve.install-from-iso
name: install-from-iso
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [install, iso, usb, installer, pveperf]
level: intro
status: docs-checked
description: "Install Proxmox VE from the hybrid ISO, write it to USB with dd, and know the minimum and recommended hardware."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pve-installation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The installer ISO is a hybrid image: burn it to optical media or copy the raw image to a USB stick, which is the recommended and faster route. It contains Debian, the Proxmox VE packages, the Proxmox kernel with KVM and LXC, and the web UI. The installer partitions the disks with ext4, XFS, BTRFS (technology preview) or ZFS, and all existing data on the selected drives is erased.

On Linux write the stick with dd, after identifying the device by comparing `lsblk` output before and after plugging it in:

```
dd bs=1M conv=fdatasync if=./proxmox-ve_*.iso of=/dev/XYZ
```

Replace `/dev/XYZ` carefully; overwriting the wrong disk is the classic mistake. Do not use UNetbootin. On Windows use Etcher, or Rufus in DD mode (answer No to the GRUB download dialog).

Boot menu choices are graphical, Terminal UI, and Terminal UI with serial console. The Terminal UI has better compatibility with very old or very new hardware, and shares the same installation code.

Evaluation minimum is a 64-bit CPU with Intel VT or AMD-V, 1 GB RAM plus guest memory, one disk and one NIC. Recommended is at least 2 GB for the OS and services plus guest memory, about 1 GB extra per TB of used storage for Ceph and ZFS, redundant SSDs (power-loss protection preferred), and redundant NICs. ZFS and Ceph are not compatible with a hardware RAID controller. Run `pveperf` for a quick CPU and disk benchmark after install.

## Checked

2026-11-09. Compared with the system requirements, installation media and installer sections of https://pve.proxmox.com/pve-docs/chapter-pve-installation.html. Removed the Secure Boot before 8.1 statement, which the page does not make (it mentions Secure Boot only for the memtest86+ entry).

Method: documentation only; no commands were run.

