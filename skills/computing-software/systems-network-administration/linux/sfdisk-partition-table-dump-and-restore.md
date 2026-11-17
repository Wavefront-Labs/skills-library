---
id: computing-software.systems-network-administration.linux.sfdisk-partition-table-dump-and-restore
name: sfdisk-partition-table-dump-and-restore
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, partitioning, sfdisk, sfdisk-dump, partition-table-backup, scripted-partitioning, disk-cloning, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Back up, restore and replicate partition tables with sfdisk dumps, script partitioning from a text spec, and move or resize partitions — for MBR and GPT alike."
sources:
  - https://github.com/util-linux/util-linux/blob/master/disk-utils/sfdisk.8.adoc
  - https://github.com/util-linux/util-linux/blob/master/disk-utils/partx.8.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sfdisk: dump, restore, script

**Goal:** keep a restorable copy of every disk's partition table, clone layouts between
disks, and partition in scripts with a readable spec.

## 1. Dump and restore
```bash
sfdisk -d /dev/sda > sda.sfdisk            # text dump: label, label-id, each partition start/size/type/uuid/name
sfdisk /dev/sda < sda.sfdisk               # restore exactly (same GUIDs/UUIDs)
sfdisk -d /dev/sda | sfdisk /dev/sdb       # clone layout to another disk (same or larger size)
sfdisk --backup -O /root/sda-pt.bak /dev/sda ...   # first save the raw partition-table sectors (device name and offset are appended to the -O name)
```
Example dump (GPT):
```
label: gpt
label-id: 6F2A…
device: /dev/sda
unit: sectors
first-lba: 2048
/dev/sda1 : start=2048, size=1048576, type=C12A7328-F81F-11D2-BA4B-00A0C93EC93B, uuid=…, name="EFI"
/dev/sda2 : start=1050624, size=208664576, type=E6D6D379-F507-44C2-A23C-238F2A3DF928, uuid=…
```
Cloning with the dump copies partition/disk UUIDs too — remove the `uuid=` and `label-id:`
lines (or change them afterwards with `sfdisk --disk-id` and `--part-uuid`) when the two disks will live in the same machine.
Store dumps off-host (config management, backup) — after an accidental `mklabel` they make
recovery a one-liner.

## 2. Scripted partitioning
```bash
sfdisk /dev/sdb <<'EOF'
label: gpt
size=512MiB, type=uefi, name=EFI
size=4GiB,   type=swap
             type=lvm
EOF
```
Omitted start = next aligned free space; omitted size = rest of the disk. Type aliases:
`linux`, `swap`, `lvm`, `raid`, `uefi`, `home`, and shortcuts such as `L`, `S`, `U`, `R`, `V`, `H`. MBR: `label: dos` and
hex types (`type=83`).

## 3. Single-partition edits
```bash
sfdisk --part-type /dev/sdb 3 raid
sfdisk --part-label /dev/sdb 1 EFI
echo ', +' | sfdisk -N 3 /dev/sdb        # grow partition 3 to fill free space after it
sfdisk --delete /dev/sdb 4
echo '+10GiB,' | sfdisk --move-data /dev/sdb -N 2   # move partition start right AND move its data (slow, back up!)
sfdisk --no-reread --no-act …                       # dry run
```

## Gotchas
- Fed from a script or pipe, sfdisk applies the input (it prompts only when run on a terminal); rehearse with `--no-act`.
- Restoring a dump onto a smaller disk fails if the last partition doesn't fit; edit sizes.
- In-use disks: "Device busy" re-read warnings → `partx -u` after.

## Verify
- [ ] `sfdisk -d` of the target diffs cleanly against the source dump (except intended uuid changes).
- [ ] Dumps for every server disk exist in your backup/config store.

## Checked
Checked 2026-10-26 against the util-linux master sfdisk(8) man page source.
Confirmed: `-d/--dump` and restore from stdin, `--backup` with `-O`, dump header fields (label, label-id, unit, first-lba), `--delete`, `--part-type`, `--part-label`, `--disk-id`, `--part-uuid`, `-N`, `'+'` to enlarge a partition, `--move-data` with `-N`, `--no-act`, `--no-reread`; type aliases linux, swap, lvm, raid, uefi, home with their GPT GUIDs; omitted start and size defaults; BLKRRPART behaviour on in-use devices.
Removed as unconfirmed: the sgdisk and partprobe suggestions and the E shortcut (deprecated in favour of Ex).
Method: documentation only; no commands were run.
