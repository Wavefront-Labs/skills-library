---
id: computing-software.systems-network-administration.linux.sgdisk-scripted-gpt-partitioning
name: sgdisk-scripted-gpt-partitioning
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, partitioning, sgdisk, gdisk, gpt, gpt-backup, partition-guid, mbr-to-gpt, gpt-repair, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Script and repair GPT tables with sgdisk/gdisk: create partitions with type codes, back up and replicate tables between disks, convert MBR to GPT and fix damaged headers."
sources:
  - https://man.archlinux.org/man/sgdisk.8
  - https://www.rodsbooks.com/gdisk/sgdisk-walkthrough.html
  - https://www.rodsbooks.com/gdisk/repairing.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# sgdisk / gdisk for GPT

**Goal:** non-interactive, repeatable GPT layouts for provisioning, and recovery when a GPT
header or table is damaged.

## 1. Create a layout in one command
```bash
sgdisk --zap-all /dev/sdb                                       # wipe GPT + protective MBR
sgdisk -n 1:1MiB:+512MiB -t 1:ef00 -c 1:EFI \
       -n 2:0:+1GiB      -t 2:8300 -c 2:boot \
       -n 3:0:0          -t 3:8e00 -c 3:lvm  /dev/sdb           # 0 = next free / end of disk
sgdisk -p /dev/sdb
partprobe /dev/sdb
```
gdisk type codes are 4-hex shorthands: `8300` Linux filesystem (the default on Linux), `8200` swap, `8e00` LVM,
`ef00` EFI System, `ef02` BIOS boot. `sgdisk -L` lists all.
Change later: `sgdisk -t 3:8300 /dev/sdb`.

## 2. Backup, restore, replicate
```bash
sgdisk --backup=sdb-gpt.bin /dev/sdb          # protective MBR + both headers + table
sgdisk --load-backup=sdb-gpt.bin /dev/sdb     # restore
sgdisk -R /dev/sdc /dev/sdb                   # copy sdb's table TO sdc (note argument order!)
sgdisk -G /dev/sdc                            # new random disk+partition GUIDs (required after -R)
```
Typical: replacing a failed RAID member — replicate from the healthy disk, randomise GUIDs,
then `mdadm --add`.

## 3. Repair
GPT keeps a primary header at the start and a backup at the end of the disk.
```bash
sgdisk -v /dev/sdb               # verify: reports CRC mismatches, overlaps, header problems
sgdisk -e /dev/sdb               # move backup structures to the (new) end — after growing a LUN
gdisk /dev/sdb                   # interactive: r (recovery) → b use backup header / c load backup table / w
```

## 4. MBR → GPT conversion
```bash
sgdisk -g /dev/sdb               # convert in place (needs free space at start/end for GPT structures)
```
For a boot disk, add a BIOS boot partition (`ef02`) or ESP and reinstall GRUB afterwards.
Back up first; test on a copy.

## Gotchas
- `sgdisk -R` argument order is target first (`-R=/dev/target /dev/source`) — reversing it
  overwrites the good disk.
- Hybrid MBRs (`-h`) are fragile; avoid unless an old OS needs them.
- After cloning disks with identical GUIDs, udev `by-partuuid` links collide — always `-G`.

## Verify
- [ ] `sgdisk -v /dev/sdb` reports "No problems found".
- [ ] `lsblk -o NAME,PARTUUID,PARTTYPENAME,PARTLABEL` shows unique GUIDs and the intended types.

## Checked

Documentation check. Checked 2026-10-27 against the sgdisk(8) page (man.archlinux.org) and the Rod Smith gdisk/sgdisk pages (rodsbooks.com): `-Z`/`--zap-all`, `-b`/`--backup` (protective MBR, headers and table), `-l`/`--load-backup`, `-R`/`--replicate` (copies the main device's table to the named second device, with all GUIDs), `-G` (randomise GUIDs, after cloning), `-e` (move backup structures to the disk end), `-g` (MBR to GPT), `-h` (hybrid MBR), `-L`, and the type codes 8300, 8200, 8e00, ef00 and ef02. Removed the `fd00` and `8304` codes, which the sources do not show.
Method: documentation only; no commands were run.
