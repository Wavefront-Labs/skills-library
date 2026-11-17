---
id: computing-software.systems-network-administration.virtualisation.ceph-health-warnings-and-noout-maintenance
name: ceph-health-warnings-and-noout-maintenance
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ceph-health, ceph-noout, ceph, health-detail, pg-states, slow-ops, scrub-errors, node-maintenance, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Read Ceph health on Proxmox: common HEALTH_WARN causes and fixes (slow ops, inconsistent PGs, nearfull, clock skew), PG states, and noout for node maintenance."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/health-checks/
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pve_ceph_maintenance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ceph health warnings and noout maintenance

**Goal:** know which Ceph warnings need action now, and reboot nodes without triggering
pointless data rebalancing.

## Read health
```sh
ceph -s
ceph health detail
ceph pg dump_stuck     # optionally: unclean|inactive|stale|undersized|degraded
```

## Common warnings
| Warning | Usual cause | Action |
|---|---|---|
| `OSD_DOWN` / `PG_DEGRADED` | Disk, node or network | Find the OSD; replace or bring up |
| `SLOW_OPS` | Extreme load, a slow storage device or a software bug | On the OSD host: `ceph daemon osd.<id> ops` and `dump_historic_ops`; check that disk and the network |
| `PG_DAMAGED` / `OSD_SCRUB_ERRORS` | Scrub found inconsistent PGs (`active+clean+inconsistent`) | `ceph pg repair <pgid>` after checking disk health |
| `OSD_NEARFULL` / `POOL_NEAR_FULL` | Capacity or pool quota | Add capacity, delete data; don't raise ratios casually |
| `MON_CLOCK_SKEW` | Monitor host clocks not synchronised | Fix time sync (NTP/chrony) on monitor hosts |
| `RECENT_CRASH` | A daemon crashed recently | `ceph crash ls-new`, investigate, then `ceph crash archive-all` |

PG states to worry about: stuck `inactive` PGs cannot serve reads or writes, and `incomplete` can follow a PG that cannot be backfilled.
`degraded`, `undersized` and `backfilling` indicate recovery in progress; `backfill_toofull` means a backfill could not complete for lack of space.

## Node maintenance with noout
```sh
ceph osd set noout          # stop OSDs being marked out while down
# (optionally) ceph osd set norebalance
# migrate VMs away, reboot the node, wait for its OSDs to rejoin
ceph -s                     # all OSDs up, PGs active+clean
ceph osd unset noout
```
In the PVE GUI the global flags are under Ceph -> OSD -> Manage Global Flags. Ceph also supports per-scope flags, for example `ceph osd set-group noup,noout host-<name>` and `ceph osd unset-group noup,noout host-<name>`. While `noout` is set, a down OSD is never marked out (and `OSDMAP_FLAGS` warns), so a real failure would not self-heal: unset it afterwards, one node at a time.

## Gotchas
- `ceph pg repair` overwrites the digest of the inconsistent copy with that of the authoritative copy chosen by the scrub; it does not solve every problem, so check the disks under the PG first.
- Mute with a time limit, for example `ceph health mute <CODE> 1w`; `--sticky` keeps the mute when the alert changes.

## Verify
`ceph -s` shows `HEALTH_OK` (or only understood, muted-with-TTL warnings), and `ceph health detail` shows no `OSDMAP_FLAGS` warning for noout after maintenance.

## Checked

2026-10-26. Documentation checked: Ceph docs and option definitions (src/common/options) on ceph/ceph master (last commit 2026-10-25), pveceph(1) man page for PVE 9.2.13 and the pveceph.adoc source. Confirmed: health check names (OSD_DOWN, PG_DEGRADED, SLOW_OPS, PG_DAMAGED, OSD_SCRUB_ERRORS, OSD_NEARFULL, POOL_NEAR_FULL, MON_CLOCK_SKEW, RECENT_CRASH), ceph crash ls-new and archive-all, pg dump_stuck, osd flags and set-group, health mute with duration and --sticky, pg repair semantics, noout in the PVE shutdown procedure. Corrected: PG_INCONSISTENT, POOL_NEARFULL and POOL_NO_REDUNDANCY are not health check names in the Ceph docs; removed the unconfirmed per-node GUI noout claim and ceph osd perf.

Method: documentation only; no commands were run.
