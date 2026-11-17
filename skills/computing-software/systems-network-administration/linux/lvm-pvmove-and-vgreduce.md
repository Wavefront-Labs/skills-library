---
id: computing-software.systems-network-administration.linux.lvm-pvmove-and-vgreduce
name: lvm-pvmove-and-vgreduce
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, lvm, pvmove, vgreduce, pvremove, disk-migration, storage-migration, online-migration, rhcsa, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Migrate data off a disk online with pvmove, then remove it from the volume group with vgreduce/pvremove — for array migrations, failing disks and shrinking VGs."
sources:
  - https://github.com/lvmteam/lvm2/blob/main/man/pvmove.8_pregen
  - https://github.com/lvmteam/lvm2/blob/main/man/vgreduce.8_pregen
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pvmove and vgreduce

**Goal:** move logical volumes from an old disk/LUN to a new one while filesystems stay
mounted and services keep running, then retire the old disk.

## 1. Plan
```bash
pvs -o pv_name,vg_name,pv_size,pv_free,pv_used
pvdisplay -m /dev/sdb1          # which LV extents live on this PV
lvs -o lv_name,devices vg0      # LV → PV mapping
```
Need free extents ≥ used extents of the source PV on the other PVs in the VG.

## 2. Migrate
```bash
pvcreate /dev/sdd1
vgextend vg0 /dev/sdd1
pvmove /dev/sdb1 /dev/sdd1              # move everything from sdb1 to sdd1
pvmove -n lv_data /dev/sdb1 /dev/sdd1   # just one LV
pvmove -b /dev/sdb1                     # background, any free PV as destination
lvs -a -o name,copy_percent,devices vg0 # progress
pvmove                                  # resume after crash/reboot (no args)
pvmove --abort                          # stop; with --atomic all LVs stay on the source PV
```
pvmove checkpoints its progress, so an interrupted move can be restarted; `--atomic` makes it all-or-nothing. It adds I/O load — schedule off-peak.

## 3. Remove the old PV
```bash
pvs /dev/sdb1                           # PFree == PSize (no extents used)
vgreduce vg0 /dev/sdb1
pvremove /dev/sdb1                      # wipe LVM label
# then wipefs, remove from multipath/SAN zoning, detach
```

## 4. Failed disk (PV missing)
```bash
vgs -o +vg_missing_pv_count
vgreduce --removemissing vg0            # refuses if LVs use the missing PV
vgreduce --removemissing --force vg0    # removes LVs that lived on it — data loss for those
lvconvert --repair vg0/lv_raid          # RAID/mirror LVs: rebuild onto free space instead
```

## Gotchas
- After an interruption, rerun `pvmove` with no PV arguments to restart from the last checkpoint.
- `vgreduce --removemissing --force` also removes the parts of those LVs (and dependent snapshots) that sit on disks that are still present.

## Verify
- [ ] `pvdisplay -m /dev/sdb1` shows only free extents before vgreduce.
- [ ] `lvs -o +devices` lists only the new PV(s); filesystems still mounted and consistent.
- [ ] `pvs` no longer lists the old disk after pvremove.

## Checked

Checked against the lvm2 main branch (pvmove(8), vgreduce(8) pregen), repository last pushed 2026-10-09.
Confirmed: `-n` (move only the named LV), `-b`/`--background`, `--abort`, `--atomic`, restart by running pvmove with no PV arguments, `vgreduce --removemissing` and its `--force` behaviour.
Removed unconfirmed claims: segment-by-segment mirroring, snapshot and thin-pool movement rules, lvmlockd exclusivity, and that completed segments stay moved after an abort (it depends on `--atomic`).

Method: documentation only; no commands were run.
