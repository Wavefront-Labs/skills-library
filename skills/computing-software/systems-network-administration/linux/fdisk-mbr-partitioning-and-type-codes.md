---
id: computing-software.systems-network-administration.linux.fdisk-mbr-partitioning-and-type-codes
name: fdisk-mbr-partitioning-and-type-codes
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, partitioning, fdisk, fdisk-mbr, dos-label, mbr, extended-partition, partition-types, partition-type-codes, lvm-partition, raid-partition, rhcsa, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Partition disks interactively with fdisk: MBR (dos) vs GPT labels, primary/extended/logical limits, setting type codes (Linux, LVM, RAID, swap, ESP) and writing safely."
sources:
  - https://github.com/util-linux/util-linux/blob/master/disk-utils/fdisk.8.adoc
  - https://github.com/util-linux/util-linux/blob/master/disk-utils/sfdisk.8.adoc
  - https://github.com/util-linux/util-linux/blob/master/disk-utils/partx.8.adoc
  - https://github.com/util-linux/util-linux/blob/master/libfdisk/src/gpt.c
  - https://github.com/util-linux/util-linux/blob/master/libfdisk/src/dos.c
  - https://github.com/util-linux/util-linux/blob/master/disk-utils/fdisk-menu.c
  - https://github.com/uapi-group/specifications/blob/main/specs/discoverable_partitions_specification.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fdisk, MBR and partition type codes

**Goal:** create the partitions you need with the right type, on the right disk, and know
when MBR's limits mean you should use GPT instead.

## 1. Before touching anything
```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL,SERIAL
fdisk -l /dev/sdb               # label type (dos/gpt), sector size, existing partitions
```
Confirm the device by size/serial — `sdX` names can change between boots.

## 2. MBR (dos label) facts
- Max disk addressable: 2 TiB (512-byte sectors). Bigger disks → GPT.
- 4 primary partitions max (fdisk reports "All primary partitions have been defined already"); or 3 primary + 1
  **extended** containing **logical** partitions.
- Type is a 1-byte hex code.

## 3. Interactive session
```text
fdisk /dev/sdb
  o        new empty DOS label   (g = new GPT label)
  n        new partition → p/e, number, first sector (default aligned), last: +20G
  t        change type → partition number → hex code, GUID or alias (l at the main prompt lists known types)
  a        toggle bootable flag (MBR only)
  p        print — check before writing
  w        write and exit        (q = quit without saving)
```
Common type codes:
| Use | MBR code | GPT (fdisk alias / GUID) |
|---|---|---|
| Linux filesystem | `83` | `linux` 0FC63DAF-8483-4772-8E79-3D69D8477DE4 |
| Linux swap | `82` | `swap` 0657FD6D-A4AB-43C4-84E5-0933C84B4F4F |
| Linux LVM | `8e` | `lvm` E6D6D379-F507-44C2-A23C-238F2A3DF928 |
| Linux RAID | `fd` | `raid` A19D880F-05FC-4D3B-A006-743F0F84911E |
| EFI System | `ef` | `uefi` C12A7328-F81F-11D2-BA4B-00A0C93EC93B |
| Extended | `05` (alias `extended`) | — |
The type code is a label; Linux will mount/use a partition regardless — but installers,
systemd's GPT auto-discovery (Discoverable Partitions Specification) and other admins rely on it. Use the correct one.

## 4. After writing
```bash
partx -u /dev/sdb                           # tell the kernel about the on-disk partitions (partx --update)
lsblk /dev/sdb
mkfs.xfs /dev/sdb1   # / pvcreate /dev/sdb2 / mkswap /dev/sdb3
```
`fdisk` is designed for humans and its output is not guaranteed stable; use `sfdisk` or `partx` for scripts.

## Gotchas
- Writing a new label (`o`/`g`) destroys the partition table; data remains but is unreachable
  until restored. Back up first: `sfdisk -d /dev/sdb > sdb.dump`.
- fdisk reports detected filesystem, RAID and partition-table signatures and, in interactive mode, asks before wiping
  them (`-w`/`-W` with `auto`, `never` or `always`); say yes only if you are repurposing the area.

## Verify
- [ ] `fdisk -l /dev/sdb` shows the intended label, sizes and type codes.
- [ ] `lsblk` shows new partitions without a reboot.

## Checked

2026-10-26. util-linux master (last commit 2026-10-26): libfdisk type aliases and codes (linux 83 and 0FC63DAF..., swap 82 and 0657FD6D..., lvm 8E and E6D6D379..., raid FD and A19D880F..., uefi EF and C12A7328..., extended 05); fdisk menu keys o, g, n, t, a, p, w, q, l; MBR 2 TiB limit and the four-primary limit in libfdisk dos.c; fdisk.8 on wiping signatures and on output stability; sfdisk --dump; partx --update; lsblk columns MODEL, SERIAL, FSTYPE and MOUNTPOINTS. UAPI Discoverable Partitions Specification for the ESP, swap and generic Linux GUIDs. Removed the BIOS boot alias row (not an fdisk alias), logical numbering from 5, partprobe and parted remarks, and the same-start-sector claim.

Method: documentation only; no commands were run.
