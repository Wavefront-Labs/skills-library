---
id: computing-software.systems-network-administration.backup-and-recovery.restoring-to-dissimilar-hardware
name: restoring-to-dissimilar-hardware
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [dissimilar-hardware, bare-metal-recovery, driver-injection, universal-restore, uefi, initramfs, restore-to-new-hardware, storage-driver-injection]
level: advanced
status: docs-checked
description: "Restore a server backup onto different hardware or a VM: storage driver injection, BIOS vs UEFI boot repair, Linux initramfs and fstab fixes, NIC and licensing changes."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/add-and-remove-drivers-to-an-offline-windows-image
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/bcdboot-command-line-options-techref-di
  - https://man7.org/linux/man-pages/man8/dracut.8.html
  - https://relax-and-recover.org/documentation/
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Restoring to dissimilar hardware

**Goal:** a backed-up server boots on replacement hardware (different model, controller or a VM) after restore.

## Before you need it
- Keep drivers for likely target hardware (storage controller, NIC) with the recovery media.
- Build recovery media that can load extra drivers: in Windows PE, `drvload` adds a driver to the running WinPE.
- Record source firmware mode (UEFI or BIOS) and disk layout.

## Windows
1. Restore the image with the backup tool's bare-metal restore; supply the new storage driver when prompted, or inject it into the restored Windows afterwards. DISM adds driver packages to an offline image, where they land in the driver store and Plug and Play binds them when the system boots:
```cmd
Dism /Image:<OFFLINE_WINDOWS_ROOT> /Add-Driver /Driver:<DRIVER_DIR> /Recurse
Dism /Image:<OFFLINE_WINDOWS_ROOT> /Get-Drivers
```
Microsoft documents this against a mounted image, from a technician machine on Windows 10 / Server 2016 or later (or WinPE of that generation). `/Recurse` can bloat the image; `/ForceUnsigned` overrides the signature requirement on x64. Removing a boot-critical driver can make an image unbootable.
2. If the new machine boots differently (BIOS to UEFI), the restored disk must match: restore with a GPT disk and EFI system partition, then rebuild boot files:
```cmd
bcdboot <RESTORED_WIN>\Windows /s S: /f UEFI
```
`/s` names the system-partition volume letter, and `/f` (UEFI, BIOS or ALL) requires `/s`. BCDBoot copies boot files from the Windows directory to the system partition and creates the BCD store; on UEFI it also adds a firmware NVRAM entry unless `/s` is used.
3. After boot: install remaining drivers; remove ghost NICs and re-apply static IPs; check activation (hardware change can trigger reactivation) and licence-bound software.

## Linux
1. Restore files and partitions. Relax-and-Recover (ReaR) is a Linux recovery tool; its user guide has Layout Configuration and scenario chapters for recreating disk layouts.
2. Chroot into the restored system (bind-mount `/dev`, `/proc`, `/sys` first), then rebuild the initramfs without host-only mode on dracut-based distributions:
```bash
dracut -f --regenerate-all --no-hostonly
```
A host-only initramfs contains only the modules needed for the machine it was built on, so the disk cannot be moved to another controller or machine without recreating it; `-f` overwrites the existing image and `--regenerate-all` rebuilds the image for every installed kernel. Other distributions use their own tool (for example update-initramfs on Debian-family systems); check its documentation.
3. Reinstall or repair the boot loader for BIOS or UEFI as your distribution documents.
4. Check `/etc/fstab` uses UUIDs that exist (`blkid`); fix network interface names and MAC-bound configs.

## Restore to a VM instead
Often fastest: many tools restore physical backups directly to vSphere/Hyper-V/cloud VMs, handling drivers. Use it to meet RTO while hardware is replaced.

## Verify
Annual test: restore a production server's backup onto a different model or a VM and record the extra steps needed in the DR runbook.

## Checked
2026-11-08. Confirmed against the DISM offline driver page, BCDBoot options page and dracut man page (read in full for the relevant sections) and the ReaR documentation index (index only; chapter contents not read). Removed unsupported claims: Veeam recovery media drivers, ReaR interactive layout mapping, the update-initramfs/grub2-install/efibootmgr commands, and the exact mount commands. Activation, ghost-NIC and fstab advice is general practice and not documented in the cited pages.
Method: documentation only; no commands were run.
