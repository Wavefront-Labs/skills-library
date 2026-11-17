---
id: computing-software.systems-network-administration.virtualisation.ceph-nearfull-osds-and-balancer
name: ceph-nearfull-osds-and-balancer
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [osd-nearfull, ceph-balancer, ceph, pveceph, ceph-health, capacity, proxmox]
level: advanced
status: docs-checked
description: "Handle Ceph OSD_NEARFULL, BACKFILLFULL and FULL on Proxmox: ratios, upmap balancer, reweighting, freeing space, and capacity rules so one node loss still fits."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/health-checks/
  - https://docs.ceph.com/en/latest/rados/operations/balancer/
  - https://docs.ceph.com/en/latest/rados/operations/monitoring-osd-pg/
  - https://pve.proxmox.com/pve-docs/chapter-pveceph.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ceph nearfull/full OSDs and the balancer

## Thresholds (defaults)
| Ratio | Default | Effect |
|---|---|---|
| `nearfull_ratio` | 0.85 | HEALTH_WARN OSD_NEARFULL |
| `backfillfull_ratio` | 0.90 | backfill to that OSD refused (recovery stalls) |
| `full_ratio` | 0.95 | the cluster is flagged full and cannot serve writes: VMs hang |

These are the initial values set when the cluster is created (`mon_osd_nearfull_ratio`, `mon_osd_backfillfull_ratio`, `mon_osd_full_ratio`); the live values are in `ceph osd dump | grep full_ratio` and are changed with `ceph osd set-nearfull-ratio`, `set-backfillfull-ratio` and `set-full-ratio`. OSD_NEARFULL is raised per OSD, so one fullest OSD is enough.

## Diagnose
```sh
ceph health detail
ceph osd df               # utilisation, variance and PG count per OSD
ceph df                   # pool usage per pool
ceph balancer status
```

## Fix imbalance (most nearfull cases)
```sh
ceph balancer mode upmap          # the default mode; needs all clients Luminous or newer: ceph osd set-require-min-compat-client luminous
ceph balancer status              # in upmap mode automatic balancing is enabled
ceph balancer eval                # score for the current distribution (also: eval <pool>)
```
`ceph balancer off` disables it; `crush-compat` mode is the option for older clients. Prefer the upmap balancer over manual reweighting.

## Already FULL (writes blocked)
1. Short-term workaround: raise the full threshold by a small amount with `ceph osd set-full-ratio <ratio>`; this restores write availability but is not a fix.
2. Free space: delete unneeded snapshots and old VM disks, and remove test pools. Leftover `rados bench` objects (names starting with `bench`) in a pool can be removed very carefully by hand.
3. Add OSDs in appropriate CRUSH failure domains. Restore the ratio afterwards (default 0.95).
Do not delete objects at the RADOS layer except such known test objects.

## Capacity rule
Keep enough headroom that losing one host does not push the survivors past nearfull: the Proxmox guide notes that a single OSD failure forces Ceph to recover more data at once and tells you to stay well below `nearfull_ratio` (default 85%). As a rough calculation with size=3 across N equal hosts, usable data should stay below (N-1)/N x 0.85 of raw/3 (about 64% for four hosts); this is arithmetic, not a documented figure.

## Gotchas
- With too few PGs the balancer has less to work with; the PG autoscaler (pool mode `warn`, `on` or `off`; `pveceph pool create --pg_autoscale_mode`) adjusts `pg_num` when it is off by a factor of 3.
- Recovery after an OSD failure can push survivors to backfillfull (a backfill is refused at `backfill_full_ratio`, state `backfill_toofull`): that is why headroom matters.

## Verify
`ceph osd df` shows evenly used OSDs, `ceph balancer eval` score improves, and no NEARFULL warning remains in `ceph health detail`.

## Checked

2026-10-26. Documentation checked: Ceph docs and option definitions (src/common/options) on ceph/ceph master (last commit 2026-10-25), pveceph(1) man page for PVE 9.2.13 and the pveceph.adoc source. Confirmed: ratio defaults 0.85/0.90/0.95 (option definitions), set-*-ratio commands, OSD_FULL workaround, bench objects in full-pool advice, balancer modes (upmap default, crush-compat, read, upmap-read), set-require-min-compat-client luminous, balancer eval and off, backfill_toofull and backfill_full_ratio, autoscaler factor of 3 and modes. Removed unconfirmed: reweight-by-utilization, osd df tree and VAR thresholds, MAX AVAIL semantics, 70% alert, PG per OSD minimum.

Method: documentation only; no commands were run.
