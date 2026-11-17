---
id: computing-software.systems-network-administration.linux.move-or-rename-volume-groups
name: move-or-rename-volume-groups
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, lvm, vgexport, vgimport, vgrename, vgimportclone, vgsplit, disk-migration]
level: advanced
status: docs-checked
description: "Move LVM volume groups between hosts and resolve name or UUID clashes: vgexport/vgimport, vgrename (and fixing fstab/GRUB for root), vgimportclone for cloned disks, vgsplit."
sources:
  - https://github.com/lvmteam/lvm2/blob/main/man/vgexport.8_pregen
  - https://github.com/lvmteam/lvm2/blob/main/man/vgimport.8_pregen
  - https://github.com/lvmteam/lvm2/blob/main/man/vgrename.8_pregen
  - https://github.com/lvmteam/lvm2/blob/main/man/vgsplit.8_pregen
  - https://github.com/lvmteam/lvm2/blob/main/man/vgimportclone.8_pregen
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Moving and renaming volume groups

## Move disks to another host
```bash
# source
umount /data && vgchange -an vg_data && vgexport vg_data
# move disks / re-attach volumes
# target
pvscan ; vgimport vg_data && vgchange -ay vg_data && mount /dev/vg_data/lv_data /data
```
`vgexport` marks the VG as exported so nobody activates it by accident mid-move. Attaching the same
shared LUN to several hosts needs lvmlockd or system IDs (see lvmlockd(8) and lvmsystemid(7)); plain LVM does not coordinate between hosts.

## Name clash on import
Target already has `vg_data` → `vgrename <VG UUID> vg_data_old` (use `vgs -o +vg_uuid`; the UUID form
disambiguates duplicates).

## Cloned disks (same PV/VG UUIDs: snapshots, dd copies, cloud volume clones)
`vgimportclone --basevgname vg_restore /dev/sdc` — generates new UUIDs and a new VG name so both
can be active together. Without it LVM warns about duplicate PVs.

## Renaming the root VG (harder)
```bash
vgrename rhel vg_sys
```
Every reference to the old name must then be updated: `/etc/fstab`, the kernel command line, any `resume=` setting, and the initramfs. Those steps are distribution-specific (see your distribution's bootloader and initramfs documentation). Keep rescue media handy.

## Split a VG
`vgsplit vg_big vg_new /dev/sdd` moves PVs into a new VG. LVs cannot be split between VGs: each LV must be entirely on the PVs in the source or the destination VG.

## Verify
- [ ] `vgs`/`lvs` show expected names and no duplicate-PV warnings; reboot mounts everything.

## Checked

Checked against the lvm2 main branch (vgexport(8), vgimport(8), vgrename(8), vgsplit(8), vgimportclone(8) pregen), repository last pushed 2026-10-09.
Confirmed: vgexport puts the VG in an exported state so it cannot be used until imported; renaming by VG UUID when two VGs share a name; `vgimportclone --basevgname`; the vgsplit rule that no LV can span the two VGs.
Removed unconfirmed claims: the RHEL-specific root-VG rename commands (fstab, grubby, dracut), the quoted duplicate-PV warning text, and that vgsplit needs inactive LVs.

Method: documentation only; no commands were run.
