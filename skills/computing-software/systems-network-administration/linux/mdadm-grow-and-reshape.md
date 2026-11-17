---
id: computing-software.systems-network-administration.linux.mdadm-grow-and-reshape
name: mdadm-grow-and-reshape
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, mdadm, software-raid, mdadm-grow, raid-grow, reshape, raid-level-change, raid5-to-raid6, larger-disks, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Grow mdadm arrays online: add devices to RAID5/6, migrate to larger disks, change level (RAID1→5, RAID5→6), with backup files, reshape monitoring and filesystem resize."
sources:
  - https://github.com/md-raid-utilities/mdadm/blob/main/mdadm.8.in
  - https://github.com/md-raid-utilities/mdadm/blob/main/md.4
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mdadm --grow: more disks, bigger disks, other levels

**Goal:** add capacity or redundancy to a live md array without rebuilding from backup —
while knowing that a reshape is the riskiest md operation and needs a backup first.

## 1. Add a disk to RAID5/6 (more members)
```bash
mdadm --add /dev/md0 /dev/sde1                          # becomes a spare
mdadm --grow /dev/md0 --raid-devices=5 --backup-file=/root/md0-grow.bak   # reshape 4 → 5
cat /proc/mdstat                                        # reshape = 3.1% … finish=…
```
During the "critical section" mdadm disables writes and takes a backup of that data. For grows the backup may be kept on a spare device or in a `--backup-file` (which cannot be on the array being reshaped); the file is required for shrinks, RAID level changes and layout changes. Afterwards grow the layer above.

## 2. Replace all members with larger disks
One at a time: `--replace` (or fail/remove/add) each disk with a bigger one, partition it
larger, wait for each rebuild to finish. Then (the "size" is taken from the smallest member until you do; growing it starts a resync of the new space):
```bash
mdadm --grow /dev/md0 --size=max        # use the new space
```

## 3. Change level
```bash
mdadm --add /dev/md0 /dev/sdc1                                     # spare first
mdadm --grow /dev/md0 --level=5 --raid-devices=3                   # RAID1 (2 disks) → RAID5 (3)
mdadm --add /dev/md0 /dev/sdf1
mdadm --grow /dev/md0 --level=6 --raid-devices=5 --backup-file=/root/md0.bak   # RAID5 (4) → RAID6 (5)
mdadm --grow /dev/md0 --level=0                                    # RAID10 (near-2 layout) → RAID0 (loses redundancy)
```
Supported conversions: RAID1 and RAID5, RAID5 and RAID6, RAID0/RAID4/RAID5, and RAID0 and RAID10 (near-2). The level change itself is instant, but RAID5 to RAID6 needs a non-standard layout that is changed afterwards and can take a long time, and a `--backup-file` is required.

## 4. Grow what's on top
```bash
pvresize /dev/md0                 # LVM PV
xfs_growfs /mountpoint            # XFS
resize2fs /dev/md0                # ext4 directly on md
```
Update the ARRAY line in `/etc/mdadm.conf` (or `/etc/mdadm/mdadm.conf`) if it records `num-devices` or level, and regenerate your initramfs if it embeds mdadm.conf (distribution-specific).

## 5. Interrupted reshape
If the system crashed during the critical section, pass the same backup file to `--assemble`:
`mdadm --assemble /dev/md0 --backup-file=/root/md0-grow.bak /dev/sd[b-e]1`
(if the backup file is lost, an empty file plus `--invalid-backup` is a last resort: the data being rearranged at the crash may be lost).

## Gotchas
- Back up before reshaping — a power loss or second disk failure mid-reshape is the worst case.
- Removing a write-intent bitmap (`--bitmap=none`) before a grow is commonly done and re-adding it afterwards; see mdadm(8) GROW MODE.
- Supported chunk-size/layout changes apply to RAID0, RAID4, RAID5, RAID6 and RAID10.

## Verify
- [ ] `mdadm --detail /dev/md0` shows the new Raid Level/Devices and Array Size, State clean.
- [ ] Filesystem/PV size grew (`df -h`, `pvs`).
- [ ] mdadm.conf and initramfs updated; reboot assembles the array.

## Checked

Checked against the mdadm main branch man page (mdadm.8.in, GROW MODE, LEVEL CHANGES, SIZE CHANGES), repository last pushed 2026-10-08.
Confirmed: the list of supported conversions; critical-section backup rules (spare device or `--backup-file`, required for shrinks, level and layout changes); `--invalid-backup` semantics; `--size=max` and the resync after growing size; `--bitmap=none` removes a bitmap in grow mode.
Fixed: the skill claimed newer mdadm does not need a backup file for level changes and listed `RAID5 to 0` as one step; the man page lists only RAID0, RAID4 and RAID5 conversions and RAID0 with RAID10 (near-2). Removed unconfirmed claims: reshape speed and RAID10 reshape remarks, and the specific initramfs commands.

Method: documentation only; no commands were run.
