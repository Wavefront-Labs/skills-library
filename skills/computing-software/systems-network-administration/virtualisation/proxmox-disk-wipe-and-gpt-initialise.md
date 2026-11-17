---
id: computing-software.systems-network-administration.virtualisation.proxmox-disk-wipe-and-gpt-initialise
name: proxmox-disk-wipe-and-gpt-initialise
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-disk-wipe, wipefs, gpt, proxmox, storage]
level: intro
status: docs-checked
description: "Clear old signatures from a disk before reuse on Proxmox VE: wipefs options, dry run and backup, ceph-volume zap for former Ceph OSDs, and pveceph osd destroy cleanup."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#chapter_storage
  - https://man7.org/linux/man-pages/man8/wipefs.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wipe old signatures from a disk (Proxmox VE)

**Goal:** reuse a disk that still carries an old filesystem, RAID, partition table or Ceph
OSD. Wiping the wrong disk destroys its data, so check the device name twice.

## wipefs (util-linux man page)
- `wipefs <device>` with no options only lists visible signatures and their offsets (since
  v2.31 it lists every offset, as FAT, ZFS and GPT store more than one magic string).
- `wipefs -a <device>` erases all signatures libblkid can see and rescans until none are
  found. On a partitioned whole disk it erases only the partition tables, not the content of
  the partitions. It does not erase the filesystem itself or other data.
- `-n` (`--no-act`) does everything except the write, so use it first as a dry run.
- `-b` (`--backup[=dir]`) saves each erased signature to `wipefs-<devname>-<offset>.bak` in
  `$HOME` or the given directory. The man page example restores one with
  `dd if=<file> of=<device> seek=$((<offset>)) bs=1 conv=notrunc`.
- `-f` (`--force`) erases even if the filesystem is mounted, and is needed to erase a nested
  partition-table signature on a non-whole-disk device.
- `-t <list>` limits which signature types are listed or erased.
- `--lock` takes an exclusive lock; the man page recommends it to avoid collisions with
  systemd-udevd.

## Former Ceph OSD disk
The Proxmox VE admin guide: if the disk was in use before (for example for ZFS or as an
OSD) zap all traces before `pveceph osd create /dev/sd[X]`:
```sh
ceph-volume lvm zap /dev/sd[X] --destroy
```
The guide warns this destroys all data on the disk and removes the partition table, boot
sector and OSD leftovers. When destroying an OSD in the GUI (More, Destroy) enable the
cleanup option to clean up the partition table and other structures so the disk can be
reused immediately; the CLI equivalent is `pveceph osd destroy` with `--cleanup`, which also
runs `ceph-volume lvm zap --destroy`, `pvremove` on the volume group's physical volume and
wipes leftover journal/block.db/block.wal partitions.

## Checked
Date: 2026-11-07. Read the wipefs(8) man page on man7.org in full and searched the Proxmox
VE admin guide text for disk wipe, GPT and zap content, reading the Ceph OSD section.
Removed as not on either page: the GUI "Wipe Disk" and "Initialize Disk with GPT" flow,
`sgdisk --zap-all` and `sgdisk -o` as a wipe procedure, `zpool labelclear`, the `dd` zeroing
step, `vgchange -an`/`pvremove` advice, the ZFS end-of-disk label claim, the
`/dev/disk/by-id` and `lsblk` checks, secure erase advice and the Verify step. The guide does
show `sgdisk -N 1 /dev/sdb` in the ZFS section for creating a partition; it is not used here.
Method: documentation only; no commands were run.
