---
id: computing-software.systems-network-administration.virtualisation.ceph-pools-size-and-pg-autoscaling
name: ceph-pools-size-and-pg-autoscaling
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ceph-pool, pg-autoscaler, ceph, pveceph, size-min-size, target-ratio, crush-rule, rbd, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Create Ceph RBD pools on Proxmox: size 3/min_size 2 and why not 2/1, PG autoscaler with target ratios, CRUSH rules by device class, and usable capacity maths."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pve_ceph_pools
  - https://docs.ceph.com/en/latest/rados/operations/placement-groups/
  - https://github.com/proxmox/pve-docs/blob/master/pveceph.adoc
  - https://github.com/ceph/ceph/blob/main/doc/rados/operations/placement-groups.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ceph pools: size, min_size and PG autoscaling

**Goal:** pools that keep data safe through a node failure, with placement groups sized
automatically and capacity understood.

## Create
```sh
pveceph pool create vm-pool --size 3 --min_size 2 --add_storages
pveceph pool create fast --size 3 --min_size 2 --crush_rule fast --add_storages
ceph osd pool ls detail
```
`--add_storages` adds a matching RBD storage entry to PVE.

## size and min_size
- **size 3, min_size 2** (the defaults, together with 128 PGs, when no options are given) keeps data safe if any OSD fails; Ceph rejects I/O on a PG with fewer than `min_size` replicas.
- **Do not set min_size 1**: with a single replica, I/O is allowed and can lead to data loss, incomplete PGs or unfound objects.
- Erasure-coded pools offer more usable space for the price of performance; see the erasure-coded pool skill.

## Placement groups
- The pool's PG autoscale mode defaults to `warn` in PVE (it only warns about a non-optimal PG count); set it to `on` to let Ceph scale PGs automatically (`ceph osd pool autoscale-status` shows its view).
- Set **Target Ratio** (expected share of data relative to other pools with a ratio; it takes precedence over Target Size) or **Target Size** so the autoscaler decides better, and **Min. # of PGs** for a lower bound. From the CLI: `ceph osd pool set vm-pool target_size_ratio 0.8`.
- The default initial PG count is 128. Ceph's target is `mon_target_pg_per_osd` (default 100) PGs per OSD.

## Capacity
Usable is roughly raw capacity divided by `size`, minus headroom. The default `nearfull_ratio` is 85% (the guide advises staying well below it) and OSDs refuse backfill near the backfillfull ratio (default 90%); the full ratio is set with `ceph osd set-full-ratio`. Leave enough free space for the cluster to re-replicate after losing a host.

## Gotchas
- Changing `size` on a populated pool triggers data movement.
- Use device classes and CRUSH rules to keep pools on the intended disk type (`--crush_rule`).

## Verify
`ceph osd pool ls detail` shows size 3 min_size 2 and the intended crush rule;
`ceph df` shows MAX AVAIL realistic; `ceph osd df tree` shows OSD %USE within a few percent.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09). Ceph documentation sources (ceph/ceph, doc/ directory, master).

Confirmed: defaults (128 PGs, size 3, min_size 2), the min_size 1 warning, PG autoscale mode default `warn`, Target Ratio versus Target Size semantics, Min. # of PGs, `--add_storages`, nearfull ratio default 85%; from Ceph: `mon_target_pg_per_osd` default 100, backfill full ratio default 90%, `ceph osd set-full-ratio`. The draft's claim that the autoscaler is on by default was wrong for PVE pools (default is `warn`). Removed as unconfirmed: the `--application rbd` flag, the 95% full ratio number, the capacity formula, the failure-domain `osd` remark and the uneven-host remark.

Method: documentation only; no commands were run.
