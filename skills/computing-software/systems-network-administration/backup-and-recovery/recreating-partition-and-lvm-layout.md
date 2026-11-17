---
id: computing-software.systems-network-administration.backup-and-recovery.recreating-partition-and-lvm-layout
name: recreating-partition-and-lvm-layout
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [vgcfgrestore, sfdisk-dump, bare-metal-recovery, lvm, partition-table, disk-layout]
level: advanced
status: docs-checked
description: "Save and recreate Linux disk layouts for bare-metal restores: sfdisk and sgdisk dumps, LVM metadata with vgcfgbackup/vgcfgrestore, mdadm arrays, and filesystem UUIDs."
sources:
  - https://man7.org/linux/man-pages/man8/sfdisk.8.html
  - https://man7.org/linux/man-pages/man8/vgcfgrestore.8.html
  - https://man.archlinux.org/man/sgdisk.8
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Recreating partition and LVM layout

**Goal:** rebuild the exact disk layout on new disks so a file-level backup can be restored and the system boots.

## Capture (run regularly, store with the backup)
```sh
sfdisk -d /dev/sda > /backup/layout/sda.sfdisk
sgdisk --backup=/backup/layout/sda.gpt /dev/sda
vgcfgbackup -f /backup/layout/%s.vg              # one file per VG
mdadm --detail --scan > /backup/layout/mdadm.conf
lsblk -o NAME,SIZE,TYPE,FSTYPE,UUID,MOUNTPOINT > /backup/layout/lsblk.txt
blkid > /backup/layout/blkid.txt
```
`vgcfgbackup` writes VG metadata only (not the contents of LVs), one file per VG in LVM's default backup directory, or named by `-f` where `%s` is replaced by the VG name; the man page also suggests regularly backing up LVM's system directory. `sgdisk --backup` saves the protective MBR, both GPT headers and one copy of the partition table.

## Recreate partitions
```sh
sfdisk /dev/sda < sda.sfdisk               # same or larger disk
sgdisk --load-backup=sda.gpt /dev/sda       # reverses --backup; sgdisk advises restoring only to the original disk
sgdisk -G /dev/sdb                          # randomise the disk GUID and partition GUIDs (not type codes), e.g. after cloning
```
`sfdisk -d` dumps the partition table in a form `sfdisk` can read back. sfdisk aligns partitions when sizes are given with suffixes such as MiB or left at defaults, but follows sector numbers exactly when offsets and sizes are given in sectors, so an edited dump for a different disk should use sizes you have checked.

## Recreate RAID and LVM
```sh
mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sda2 /dev/sdb2
pvcreate --uuid "<PV UUID from vg file>" --restorefile /backup/layout/vg0.vg /dev/md0
vgcfgrestore -f /backup/layout/vg0.vg vg0
vgchange -ay vg0
```
`pvcreate --uuid` is used together with `--restorefile` (a file produced by `vgcfgbackup`); the man page says `--restorefile` is compulsory with `--uuid` unless `--norestorefile` is given. Restoring VG metadata that includes thin pools needs `vgcfgrestore --force` and data loss may occur if thin metadata has changed.

## Filesystems
Recreate with the original UUIDs so fstab and bootloader match: `mkfs.ext4 -U <uuid> /dev/vg0/root` and `mkswap -U <uuid> <device>`; check the `mkfs.xfs` documentation for how to set an XFS UUID. Then restore files, reinstall the bootloader (`grub-install`, `efibootmgr`), regenerate initramfs.

## Gotchas
- Duplicate UUIDs (cloned disks beside the originals) are ambiguous; restore only onto the replacement system.
- ReaR automates this whole procedure; use it where possible and still keep the raw layout files.

## Verify
Rebuild a test VM from the layout files plus a file backup and boot it.

## Checked

Checked 2026-10-27 against the util-linux sfdisk and mkswap manuals (util-linux/util-linux), the LVM2 man page sources for vgcfgbackup, vgcfgrestore and pvcreate (lvmteam/lvm2), the mke2fs and mdadm manuals (tytso/e2fsprogs, md-raid-utilities/mdadm) and the sgdisk manual (man.archlinux.org). Confirmed: `sfdisk -d` and its alignment behaviour, `sgdisk --backup`, `--load-backup` and `-G`, `vgcfgbackup -f` with `%s` templating and metadata-only scope, `vgcfgrestore --force` for thin metadata, `pvcreate --uuid` with `--restorefile`, `mke2fs -U`, `mkswap -U` and `mdadm --detail --scan`. Removed the unconfirmed XFS UUID option, the explicit mdadm metadata version, the 4Kn remark and the `size=` omission tip.

Method: documentation only; no commands were run.
