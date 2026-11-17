---
id: computing-software.systems-network-administration.linux.parted-gpt-partitioning-and-alignment
name: parted-gpt-partitioning-and-alignment
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, partitioning, parted, parted-gpt, gpt, mklabel, partition-alignment, align-check, resizepart, rhcsa, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Partition with parted: GPT labels with mklabel, mkpart in MiB/percent units, optimal alignment and align-check, resizepart to grow a partition, and scripting with -s."
sources:
  - https://man7.org/linux/man-pages/man8/parted.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# parted: GPT and alignment

**Goal:** create correctly aligned GPT partitions (interactively or in scripts) and grow the
last partition after a disk/LUN is enlarged.

## 1. Create
```bash
parted /dev/sdb print                         # current label/partitions
parted -s /dev/sdb mklabel gpt                # DESTROYS existing table
parted -s -a optimal /dev/sdb mkpart data xfs 1MiB 100GiB
parted -s -a optimal /dev/sdb mkpart pv 100GiB 100%
parted -s /dev/sdb set 2 lvm on               # type flags: lvm, raid, swap, esp, bios_grub, boot
parted -s /dev/sdb name 1 appdata             # GPT partition name (shows as PARTLABEL)
parted /dev/sdb unit MiB print
```
- On GPT the 2nd `mkpart` arg is the **name**; on msdos it's `primary|logical|extended`.
- `fs-type` is optional; to put a filesystem on the partition run `mkfs` separately (`resizepart` does not touch the filesystem either).
- Treat every command as immediate and irreversible; check the target device first.

## 2. Alignment
Start partitions on 1 MiB boundaries (2048 × 512-byte sectors). That's a multiple of every
common physical sector, SSD erase-block and RAID stripe size.
```bash
parted /dev/sdb align-check optimal 1        # "1 aligned"
cat /sys/block/sdb/queue/optimal_io_size /sys/block/sdb/queue/physical_block_size
```
Use units `MiB`/`GiB`/`%` (not `MB`/`GB`, which are powers of 10 and produce odd starts).
"Warning: The resulting partition is not properly aligned" → change the start.

## 3. Grow a partition (disk/LUN enlarged)
```bash
# first make the kernel see the new disk size (rescan or reboot)
parted /dev/sdb print                           # GPT: answer Fix when asked about the backup header
parted -s /dev/sdb resizepart 2 100%
partprobe /dev/sdb
pvresize /dev/sdb2   # or: xfs_growfs /mount ; resize2fs /dev/sdb2
```
Shrinking: shrink the filesystem/PV **first**, then the partition — parted won't do it for you.

## Gotchas
- `-s` (script mode) never prompts and automatically answers NO to warnings such as when shrinking; add `-f` to answer "fix" to exceptions. A bad command in a script can still wipe a disk without asking.
- Running parted against a mounted disk's table works but the kernel may not re-read until `partprobe`/reboot.
- Installing GRUB to a GPT disk on a BIOS system needs a partition with the `bios_grub` flag.

## Verify
- [ ] `parted /dev/sdb align-check optimal N` says aligned for every partition.
- [ ] `lsblk -o NAME,SIZE,PARTLABEL,PARTTYPENAME /dev/sdb` matches the plan.

## Checked

Documentation check. Checked 2026-10-27 against the parted(8) page from the man-pages project (man7.org, parted of 2021 September 28): `mklabel gpt`, `mkpart` (name required for GPT, part-type only for msdos and dvh), `set N lvm on` and the flag list (including `esp` and `bios_grub`), `name`, `align-check minimal|optimal`, `-a optimal`, `resizepart` (end position, does not modify the filesystem), `-s` (never prompts, answers NO) and `-f`. Removed the 2x write-penalty figure, the growpart claim, the sysfs rescan line and the 1-2 MiB BIOS boot size, which the page does not state.
Method: documentation only; no commands were run.
