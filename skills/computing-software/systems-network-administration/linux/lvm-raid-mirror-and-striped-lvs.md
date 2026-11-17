---
id: computing-software.systems-network-administration.linux.lvm-raid-mirror-and-striped-lvs
name: lvm-raid-mirror-and-striped-lvs
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, lvm, lvm-raid, lv-mirror, lvm-striping, striped-lv, raid1, raid5, raid10, lvconvert, stripe-size, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Build redundant or faster logical volumes with LVM itself: raid1/5/6/10 and striped LVs, stripe count and size, linear-to-mirror conversion, sync monitoring and leg repair."
sources:
  - https://github.com/lvmteam/lvm2/blob/main/man/lvmraid.7_main
  - https://github.com/lvmteam/lvm2/blob/main/man/lvconvert.8_pregen
  - https://github.com/lvmteam/lvm2/blob/main/conf/example.conf.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LVM RAID, mirrors and striped LVs

**Goal:** per-LV redundancy or throughput without a separate mdadm layer, and safe recovery
when a PV fails.

## 1. Striped (RAID0-like, no redundancy)
```bash
lvcreate -n fast -L 500G -i 4 -I 64k vg0 /dev/sdb /dev/sdc /dev/sdd /dev/sde
lvs -o name,stripes,stripe_size,devices vg0/fast
```
`-i` is the number of stripes (devices), `-I` the stripe size: the amount of data written to one device before moving to the next. Losing any PV loses the LV.

## 2. RAID LVs (dm-raid, md code underneath)
```bash
lvcreate --type raid1  -m 1 -n db   -L 200G vg0                 # 2-way mirror
lvcreate --type raid10 -m 1 -i 4 -n data -L 1T vg0               # -i = total devices (min 4): 2 mirrored pairs
lvcreate --type raid5  -i 3 -n bulk -L 3T vg0                    # 3 data + 1 parity = 4 PVs
lvcreate --type raid6  -i 4 -n arch -L 4T vg0                    # 4 data + 2 parity = 6 PVs
lvconvert --type raid1 -m 1 vg0/linear_lv                        # convert a linear LV to raid1
```
`--type mirror` is the legacy implementation; `raid1` is the default for `--mirrors`.

## 3. Monitor
```bash
lvs -a -o name,segtype,copy_percent,raid_sync_action,lv_health_status,devices vg0
lvchange --syncaction check vg0/db       # scrub; then lvs -o raid_mismatch_count
```
`raid_fault_policy` in lvm.conf (`activation {}`; default `warn`) decides the reaction to a failed device: `warn` logs it and leaves `lvconvert --repair` to you; `allocate` replaces the device from spare PVs in the VG.

## 4. Repair a failed leg
```bash
lvs -a -o name,devices,lv_health_status vg0    # "partial" / "refresh needed"
lvconvert --repair vg0/db                      # rebuild onto free extents on other PVs
lvchange --refresh vg0/db                      # transient failure (disk came back)
vgreduce --removemissing vg0                   # after repair, drop the dead PV
```

## Gotchas
- Repairing onto spare space needs free extents on PVs not already used by the LV.
- raid5 with N stripes needs N+1 devices and raid6 needs N+2.

## Verify
- [ ] `copy_percent` reaches 100 and health status is empty (OK).
- [ ] `--syncaction check` completes with `raid_mismatch_count` 0.
- [ ] In a lab, failing one PV leaves the LV readable; `--repair` restores redundancy.

## Checked

Checked against the lvm2 main branch (lvmraid(7), lvconvert(8) pregen, conf/example.conf.in, lib/report/columns.h), repository last pushed 2026-10-09.
Confirmed: lvcreate raid types and stripe counts (raid5 needs N+1 devices, raid6 N+2, raid10 minimum 4 devices with `--stripes` the total device count), linear-to-raid1 takeover, `lvchange --syncaction`, `raid_mismatch_count`, `raid_sync_action`, `lv_health_status`, `lvconvert --repair`, `lvchange --refresh`, `raid_fault_policy` values and default, legacy status of `mirror`.
Fixed: the raid10 example used `-i 2` where `-i` is the total number of devices. Removed unconfirmed claims: the `lvextend -i 1` trick, typical stripe sizes, the leg-removal command, the dracut module and thin-pool remarks.

Method: documentation only; no commands were run.
