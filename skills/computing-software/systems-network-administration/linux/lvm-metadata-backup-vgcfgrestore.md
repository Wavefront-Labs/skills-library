---
id: computing-software.systems-network-administration.linux.lvm-metadata-backup-vgcfgrestore
name: lvm-metadata-backup-vgcfgrestore
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, lvm, vgcfgbackup, vgcfgrestore, lvm-metadata, lvm-archive, pvcreate-restorefile, lvm-recovery, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Recover LVM from mistakes using metadata backups: /etc/lvm/backup and archive, vgcfgbackup, vgcfgrestore to undo an lvremove/lvreduce, and rebuilding a wiped PV label."
sources:
  - https://github.com/lvmteam/lvm2/blob/main/man/vgcfgrestore.8_pregen
  - https://github.com/lvmteam/lvm2/blob/main/man/vgcfgbackup.8_pregen
  - https://github.com/lvmteam/lvm2/blob/main/man/pvcreate.8_pregen
  - https://github.com/lvmteam/lvm2/blob/main/conf/example.conf.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LVM metadata backup and vgcfgrestore

**Goal:** undo an accidental `lvremove`, bad `lvreduce` or overwritten PV header by restoring
LVM metadata — the data blocks are usually still on disk.

## 1. Where backups live
- `/etc/lvm/backup/<vg>` — latest metadata after each change.
- `/etc/lvm/archive/<vg>_NNNNN-*.vg` — metadata **before** each change, with the command in
  the `description` line. Retention: `retain_min` (default 10) and `retain_days` (default 30) in `lvm.conf` `backup {}`.
- Every PV also stores a metadata copy in its header area.
```bash
vgcfgbackup vg0                                      # write current to /etc/lvm/backup/vg0
vgcfgbackup -f /root/vg0-$(date +%F).vg vg0          # extra copy (put it off-host too)
vgcfgrestore -l vg0                                  # list archives with descriptions/times
```

## 2. Undo an accidental lvremove / lvreduce
```bash
vgcfgrestore -l vg0                                  # pick the archive whose description names the lvremove
vgchange -an vg0                                     # deactivate LVs in the VG (unmount first)
vgcfgrestore -f /etc/lvm/archive/vg0_00042-1234567.vg vg0
vgchange -ay vg0
fsck -n /dev/vg0/data  ||  xfs_repair -n /dev/vg0/data      # read-only check before mounting
```
Works as long as the freed extents haven't been reused by a new LV since. Do it immediately;
stop any automation that might allocate in the VG. Thin pools: changes to thin metadata cannot be reverted and data loss may occur if it changed; `vgcfgrestore --force` is required in that case (see vgcfgrestore(8)).

## 3. PV label/metadata destroyed (wipefs, partial overwrite)
```bash
pvs  # "Couldn't find device with uuid XXXX"
grep -A3 'pv0' /etc/lvm/backup/vg0                   # id = "XXXX-…", device hint
pvcreate --uuid "XXXX-…" --restorefile /etc/lvm/backup/vg0 /dev/sdb1
vgcfgrestore vg0
vgchange -ay vg0
```
With `--uuid`, `--restorefile` reads the vgcfgbackup file, extracts the location and size of the data on the PV and makes the new metadata consistent with it.

## Gotchas
- Restoring old metadata after you've *grown* things since loses the later changes — pick the right archive.
- Archives on the same VG's root filesystem are lost if that VG is the broken one: copy `/etc/lvm` off-host regularly.
- Never run `pvcreate` without `--uuid --restorefile` on a disk you're trying to recover.

## Verify
- [ ] `lvs vg0` shows the restored LV with the original size.
- [ ] Read-only fsck/xfs_repair reports a consistent filesystem; data spot-checks pass.
- [ ] `/etc/lvm` is included in off-host backups.

## Checked

Checked against the lvm2 main branch (vgcfgrestore(8), vgcfgbackup(8), pvcreate(8) pregen, conf/example.conf.in), repository last pushed 2026-10-09.
Confirmed: `--list`, `--file`, default backup directory under /etc/lvm, `retain_min = 10`, `retain_days = 30`, the thin-pool warning with `--force`, and `pvcreate --uuid --restorefile` semantics.
Removed: the exact archive description string (not documented) and the claim that thin metadata may need `lvconvert --repair`.

Method: documentation only; no commands were run.
