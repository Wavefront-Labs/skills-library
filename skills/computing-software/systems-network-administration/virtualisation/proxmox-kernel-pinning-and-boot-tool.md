---
id: computing-software.systems-network-administration.virtualisation.proxmox-kernel-pinning-and-boot-tool
name: proxmox-kernel-pinning-and-boot-tool
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [proxmox-boot-tool, kernel-pin, pve-upgrade, opt-in-kernel, systemd-boot, grub, proxmox]
level: practitioner
status: docs-checked
description: "Manage Proxmox VE kernels: opt-in kernels, pinning a known-good kernel after a regression, proxmox-boot-tool for ZFS/UEFI ESPs, and cleanup of old kernels."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html#sysboot
  - https://github.com/proxmox/pve-docs/blob/master/system-booting.adoc
  - https://github.com/proxmox/pve-docs/blob/master/local-zfs.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox kernels and proxmox-boot-tool

## Which kernels
Proxmox VE ships its own Linux kernel packages (`proxmox-kernel-6.X.Y-Z-pve-signed` for the signed image). `proxmox-boot-tool` keeps by default: the running kernel, the version being newly installed, the two latest installed kernels, the latest version of the second-to-last kernel series, and any manually selected kernels.
```sh
pveversion -v | grep -i kernel
proxmox-boot-tool kernel list         # kernel versions selected for ESP sync
uname -r                              # running
```

## Pin after a regression (NIC driver, passthrough breakage)
```sh
proxmox-boot-tool kernel pin <version>-pve            # pinned until you unpin
proxmox-boot-tool kernel pin <version>-pve --next-boot # boot it once only
proxmox-boot-tool refresh
proxmox-boot-tool kernel unpin                        # remove the pin
proxmox-boot-tool refresh
```
Pinning works on all Proxmox VE systems, not only those where `proxmox-boot-tool` synchronises ESPs; on systems that do not use it you can skip the `refresh`. The boot-loader menu is the other way to pick a kernel once. Remove a pin as soon as possible so that the security patches of the latest kernel apply. `unpin --next-boot` clears a pin that was set with `--next-boot`.

## proxmox-boot-tool and ESPs
On ZFS root, kernels and initrds are stored on the 512 MB EFI System Partition (ESP) of each disk; `proxmox-boot-tool` copies them to every ESP listed in `/etc/kernel/proxmox-boot-uuids` and configures the boot loader (GRUB for legacy BIOS and for UEFI with Secure Boot, `systemd-boot` for UEFI without Secure Boot). ESPs are not mounted during normal operation.
```sh
proxmox-boot-tool status
# after replacing a boot disk in rpool:
sgdisk /dev/disk/by-id/<healthy> -R /dev/disk/by-id/<new>; sgdisk -G /dev/disk/by-id/<new>
zpool replace -f rpool <old-part3> /dev/disk/by-id/<new>-part3
proxmox-boot-tool format /dev/disk/by-id/<new>-part2
proxmox-boot-tool init   /dev/disk/by-id/<new>-part2          # add 'grub' as last argument if `proxmox-boot-tool status` shows GRUB
```
The ZFS documentation lists these steps for replacing a bootable disk; `proxmox-boot-tool init` adds a line with the new ESP's UUID to `/etc/kernel/proxmox-boot-uuids`.

## Cleanup
ESPs are 512 MB, so keep the list of synced kernels short: `proxmox-boot-tool kernel remove <version>` drops a manually added kernel from the list, and a `proxmox-boot-tool refresh` is required afterwards to update all ESPs.

## Verify
`proxmox-boot-tool status` shows every ESP configured with the same kernel list; reboot
lands on the intended kernel (`uname -r`); after unpinning, updates boot the newest.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: system-booting.adoc and local-zfs.adoc Changing a failed bootable device) and confirmed the proxmox-boot-tool status, format, init (including the grub mode), refresh, kernel list, add, remove, pin, pin --next-boot and unpin subcommands, the default kernel retention rules, the ESP size and boot-loader selection, and the disk replacement steps with sgdisk and zpool replace. Removed the unconfirmed opt-in kernel package names, GRUB_DEFAULT advice and autoremove and clean steps.

Method: documentation only; no commands were run.
