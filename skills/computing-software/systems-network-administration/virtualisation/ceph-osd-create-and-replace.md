---
id: computing-software.systems-network-administration.virtualisation.ceph-osd-create-and-replace
name: ceph-osd-create-and-replace
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ceph-osd, osd-replacement, pveceph, ceph, bluestore, db-wal, device-class, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Create Ceph OSDs on Proxmox (BlueStore, separate DB/WAL, device classes) and replace a failed disk: out, wait for recovery, destroy, recreate, without data loss."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pve_ceph_osds
  - https://docs.ceph.com/en/latest/rados/operations/add-or-rm-osds/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating and replacing Ceph OSDs on Proxmox VE

**Goal:** add disks to Ceph correctly and swap failed ones while the cluster keeps
serving I/O.

## Create
```sh
ceph-volume lvm zap /dev/nvme2n1 --destroy      # wipe old data/partitions first
pveceph osd create /dev/nvme2n1
# HDD with SSD for metadata:
pveceph osd create /dev/sdd --db_dev /dev/nvme0n1 --db_dev_size 60
```
- `--db_dev_size` is in GiB; `--wal_dev` selects a block.wal device, `--crush-device-class` sets the class and `--encrypted` enables encryption. The Proxmox guide gives the default DB/WAL sizes as 10% (DB) and 1% (WAL) of OSD size and recommends a fast SSD or NVRAM for them. An OSD's DB device is shared by every OSD placed on it, so size failure domains accordingly.
- OSDs set their device class (`hdd`, `ssd`, `nvme`) automatically at startup; create CRUSH rules per class (`ceph osd crush rule create-replicated <rule-name> <root> <failure-domain> <class>`, for example `fast default host nvme`) and assign pools.

## Replace a failed OSD
1. Identify the failed OSD with `ceph osd tree` and `ceph health detail`.
2. If the OSD is still up but failing, mark it **out** so data moves off it:
   `ceph osd out <id>`; wait until `ceph -s` shows all PGs `active+clean`.
   A `down` OSD is marked out automatically after `mon_osd_down_out_interval` (default 10 minutes).
3. Before destroying, check safety: `ceph osd safe-to-destroy osd.<id>` (poll it until it succeeds), and `ceph osd ok-to-stop <id>` before stopping.
4. Stop the service (`pveceph stop --service osd.<id>`, or Stop in the GUI), then
   `pveceph osd destroy <id> --cleanup` (`--cleanup` also destroys the underlying logical volumes with `ceph-volume lvm zap --destroy`).
5. Swap the physical disk and run `pveceph osd create /dev/<new>`; Ceph backfills onto it. Ceph's own replacement procedure (`ceph osd destroy` then `ceph-volume lvm create --osd-id <id>`) keeps the OSD ID, which the pveceph path does not.

## Gotchas
- Pools default to size 3 and min_size 2 in `pveceph pool create`; take OSDs out one failure domain at a time so PGs stay active.
- Recovery competes with client I/O: choose an `osd_mclock_profile` (`balanced` is the default; `high_client_ops` or `high_recovery_ops`). With the mClock scheduler active, `osd_max_backfills` cannot be changed unless `osd_mclock_override_recovery_settings` is true.

## Verify
`ceph osd tree` shows the new OSD up/in under the right host and class; `ceph -s` returns
to `HEALTH_OK` with all PGs `active+clean`.

## Checked

2026-10-26. Documentation checked: Ceph docs and option definitions (src/common/options) on ceph/ceph master (last commit 2026-10-25), pveceph(1) man page for PVE 9.2.13 and the pveceph.adoc source. Confirmed: pveceph osd create options (--db_dev, --db_dev_size in GiB, --wal_dev, --crush-device-class, --encrypted), pveceph osd destroy --cleanup, pveceph stop, ceph osd out/safe-to-destroy/ok-to-stop, mon_osd_down_out_interval default 10 min, device class auto-detection, create-replicated syntax, mClock profiles and recovery override, pool size/min_size defaults 3/2. Removed unconfirmed systemctl stop step, the claim that BlueStore is the only backend, consumer-SSD claim and the several-hosts-at-once claim.

Method: documentation only; no commands were run.
