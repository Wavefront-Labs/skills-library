---
id: computing-software.systems-network-administration.proxmox-ve.kernel-cmdline-and-kernel-pinning
name: kernel-cmdline-and-kernel-pinning
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [kernel-pin, cmdline, grub-cmdline, update-grub, next-boot]
level: practitioner
status: docs-checked
description: "Edit the kernel command line for GRUB or systemd-boot and pin a known-good kernel version on Proxmox VE."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Where the kernel command line lives depends on the bootloader:

- GRUB: set `GRUB_CMDLINE_LINUX_DEFAULT` in `/etc/default/grub` (or a snippet in `/etc/default/grub.d`), then run `update-grub`.
- systemd-boot: put the whole command line on one line in `/etc/kernel/cmdline`, then run `proxmox-boot-tool refresh`.

Check which applies with `proxmox-boot-tool status` or `efibootmgr -v`. Reboot to apply. Find the running kernel with `uname -r`; the first two numbers select the matching kernel.org parameter documentation.

If a newer kernel breaks hardware, pin an older one instead of removing the new one:

```
proxmox-boot-tool kernel pin 5.15.30-1-pve
proxmox-boot-tool kernel pin 5.15.30-1-pve --next-boot
proxmox-boot-tool kernel unpin
proxmox-boot-tool refresh
```

A plain pin persists until unpinned. `--next-boot` boots the pinned version once, which is useful to test whether an update fixed the problem. Pinning works on all Proxmox VE systems, not only those synchronizing ESPs; if you do not use proxmox-boot-tool for ESP sync you can skip the final `refresh`.

Remove pins as soon as possible so the latest kernel security patches apply. Secure Boot has been supported out of the box since Proxmox VE 8.1; the `proxmox-secure-boot-support` meta-package pulls in the signed shim, GRUB and kernel packages, and only GRUB is supported as the bootloader.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-sysadmin.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
