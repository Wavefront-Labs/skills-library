---
id: computing-software.systems-network-administration.linux.lvm-snapshot-merge-rollback
name: lvm-snapshot-merge-rollback
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, lvm, lvconvert-merge, snapshot-merge, lvm-snapshot, rollback, pre-upgrade-snapshot]
level: advanced
status: docs-checked
description: "Roll a logical volume back to a snapshot with lvconvert --merge: sizing pre-change snapshots, root merges on next activation, thin merges and fill monitoring."
sources:
  - https://github.com/lvmteam/lvm2/blob/main/man/lvconvert.8_pregen
  - https://github.com/lvmteam/lvm2/blob/main/man/lvmthin.7_main
  - https://github.com/lvmteam/lvm2/blob/main/conf/example.conf.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LVM snapshot merge (rollback)

## Before the risky change
```bash
lvcreate -s -n root_pre -L 10G vg/root       # classic COW snapshot: size = expected change volume
lvcreate -s -n data_pre vg/thin_data         # thin pool LV: no size needed
lvs -o lv_name,origin,data_percent vg
```
Size COW snapshots for all writes until you decide (package upgrades: a few GB). Set autoextend in lvm.conf `activation {}` (needs dmeventd monitoring; threshold 100 disables it): `snapshot_autoextend_threshold = 70`, `snapshot_autoextend_percent = 20`.
Back up a separate `/boot` too, since kernel files change.

## Roll back
```bash
lvconvert --merge vg/root_pre
# if the origin is open (for example the root filesystem) the merge is deferred to its next activation
reboot                                         # root: merge starts when the origin is next activated
lvs -a vg                                      # the snapshot is removed when the merge finishes
```
If neither the origin nor the snapshot is open the merge starts immediately; otherwise it starts the first time either is activated while both are closed (for a non-root LV: stop users, `umount /data`, then `lvchange -an vg/data && lvchange -ay vg/data`).
After the merge the merged snapshot is removed and the origin has the snapshot's contents.

## Keep the change instead
`lvremove vg/root_pre` — do this soon; COW snapshots slow writes on the origin.

## Gotchas
- A thin snapshot can also be merged into its origin (`lvconvert --merge vg/thin_snap`); changes made to the origin since the snapshot are lost.
- Snapshots are not backups — same disks, same VG.

## Verify
- [ ] After merge, `lvs` no longer lists the snapshot and the origin holds the pre-change contents.

## Checked

Checked against the lvm2 main branch (lvconvert(8) pregen `--merge`, lvmthin(7) thin snapshot merge, conf/example.conf.in, lib/report/columns.h), repository last pushed 2026-10-09.
Confirmed: merge starts immediately when origin and snapshot are closed, otherwise at the next activation; the merged snapshot is removed; `snapshot_autoextend_threshold`/`percent` semantics and the dmeventd requirement; thin snapshots are created without a size and can be merged into the origin.
Removed unconfirmed claims: the quoted error messages, the RHEL snapm/boom boot-entry tip, the kernel-rollback gotcha, and the `rpm` check.

Method: documentation only; no commands were run.
