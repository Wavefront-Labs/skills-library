---
id: computing-software.systems-network-administration.backup-and-recovery.relax-and-recover-linux-bmr
name: relax-and-recover-linux-bmr
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [bare-metal-recovery, bmr, rear, relax-and-recover, rescue-iso, disk-layout, linux, disaster-recovery]
level: advanced
status: docs-checked
description: "Bare-metal recover Linux with Relax-and-Recover (ReaR): local.conf for ISO/PXE output and NETFS/backup integration, mkbackup, recovery to same or different hardware, and testing."
sources:
  - https://relax-and-recover.org/documentation/
  - https://github.com/rear/rear/blob/master/usr/share/rear/conf/default.conf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux bare-metal recovery with Relax-and-Recover (ReaR)

**Goal:** rebuild a failed Linux server onto empty hardware (or a VM) with its original
partitions, LVM, RAID, filesystems and bootloader, then restore its data.

## What ReaR does
Creates a bootable **rescue system** (ISO, USB, PXE) that contains the server's disk
layout description and the tools to recreate it, and integrates with a backup method
(its own built-in NETFS method, or an external tool such as Bacula, Bareos, TSM, NetBackup, Data Protector or Borg).

## Configure `/etc/rear/local.conf`
```bash
OUTPUT=ISO
OUTPUT_URL=nfs://backup.<domain>/export/rear
BACKUP=NETFS
BACKUP_URL=nfs://backup.<domain>/export/rear
BACKUP_PROG_EXCLUDE=("${BACKUP_PROG_EXCLUDE[@]}" '/var/tmp/*' '/srv/scratch/*')
# With an external backup tool instead:  BACKUP=BAREOS  (or BORG, etc.; data restored by that tool)
```
Run after install and after **any** storage layout change:
```sh
rear -v mkbackup        # rescue ISO + backup (built-in methods only)
rear -v mkrescue        # rescue ISO only (when another tool backs up data)
rear checklayout || rear mkrescue    # cron: checklayout exits non-zero when the disk layout or CHECK_CONFIG_FILES changed; it does not rebuild the ISO itself
```

## Recover
1. Boot the target from the rescue ISO/PXE; choose the recovery entry from the boot menu, or log in to the rescue shell.
2. `rear -v recover`: recreates partitions/LVM/MD/filesystems per the saved layout
   (interactive mapping if disks differ in size or names), restores data, reinstalls the
   bootloader.
3. Reboot, check network naming (MAC changes on new hardware), fstab UUIDs, services.

## Dissimilar hardware
Disk size differences are handled via layout mapping prompts. The default `MODULES=( 'all_modules' )` includes every kernel module of the running kernel in the rescue system so that new hardware's drivers are available, at the cost of a larger ISO; `MODULES=( 'loaded_modules' )` or an empty `MODULES=()` makes it smaller.

## Gotchas
- An out-of-date rescue ISO recreates the old layout; automate `checklayout`.
- Store ISOs off the server and off the same storage it might lose.

## Verify
Twice a year, recover a production-equivalent server into an isolated VM from its latest
ISO and backup; record time taken against the RTO.

## Checked

Checked 2026-10-27 against ReaR 2.9 (rear/rear: usr/share/rear/conf/default.conf and doc/rear.8). Confirmed: the workflows `mkbackup`, `mkrescue`, `mkbackuponly`, `checklayout` and `recover`, `checklayout` exiting non-zero when the disk layout or `CHECK_CONFIG_FILES` changed without rebuilding the rescue system, `mkbackup` being meaningful only for built-in backup methods, `BACKUP_URL` and `OUTPUT_URL` settings, `BACKUP_PROG_EXCLUDE` as an array, the external methods listed in the configuration (Bacula, Bareos, TSM, NetBackup, Data Protector, Borg and others; restic does not appear), and `MODULES=( 'all_modules' )` as the default. Removed the unconfirmed time target, Secure Boot and UEFI-versus-BIOS remarks.

Method: documentation only; no commands were run.
