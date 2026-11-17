---
id: computing-software.systems-network-administration.virtualisation.proxmox-ceph-erasure-coded-pools
name: proxmox-ceph-erasure-coded-pools
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [erasure-coded-pool, ceph, pveceph, proxmox, storage]
level: advanced
status: docs-checked
description: "Create and use erasure coded Ceph pools on Proxmox VE with pveceph, choose k and m for the node count, and understand performance and failure trade-offs."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pve_ceph_ec_pools
  - https://docs.ceph.com/en/latest/rados/operations/erasure-code/
  - https://github.com/proxmox/pve-docs/blob/master/pveceph.adoc
  - https://github.com/ceph/ceph/blob/main/doc/rados/operations/erasure-code.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Erasure coded pools on Proxmox VE Ceph

**Goal:** more usable capacity than 3x replication for bulk data, with known risks.

## Create
```bash
pveceph pool create ec-bulk --erasure-coding k=4,m=2 --failure-domain host --add_storages 1
```
This creates `ec-bulk-data` (erasure coded) and `ec-bulk-metadata` (replicated, holds RBD omap and other metadata), plus a matching PVE storage entry unless `--add_storages 0` is given. When configuring the storage by hand, set the `data-pool` parameter, otherwise the EC pool is not used for data objects. `--size`, `--min_size` and `--crush_rule` apply to the replicated metadata pool, not to the EC data pool. `size` and `crush_rule` cannot be changed on EC pools; `min_size` of the data pool can be changed later. Optional parameters: `failure-domain`, `device-class`, or `profile=<name>` to use an EC profile you created with the Ceph tools.

## Choosing k and m
- Usable ratio = k/(k+m); failures tolerated = m.
- Most EC deployments need at least k+m CRUSH failure domains (hosts or racks); Ceph recommends planning for at least k+m+1, and discourages k greater than 8. Space overhead is (k+m)/k, for example 1.5 for 4+2.
- Default `min_size`: k if m = 1, k+1 if m > 1; Ceph's documentation recommends a conservative k+2. I/O is blocked while fewer than `min_size` OSDs are available. Example from the guide: k=2,m=1 gives size 3, min_size 2; k=2,m=2 gives size 4, min_size 3.

## Trade-offs
- EC pools give more usable space than replicated pools at the price of performance; without optimisations the choice of k+m affects performance (higher values are slower).
- Ceph Tentacle adds FastEC (`allow_ec_optimizations` per pool: partial reads and writes) to improve small random I/O; it needs an EC pool, `require_osd_release` tentacle or later and a supported plugin and technique combination (see the guide).
- EC profile settings cannot be changed after creation; create a new pool with a new profile and move disks (`qm move-disk <vmid> <disk> <storage>`).

## Verify
`ceph osd pool ls detail` shows `erasure` with the profile; `ceph osd erasure-code-profile get <profile>` shows k, m, failure domain; a test VM disk on the storage runs and `ceph df` reflects the expected raw-to-usable ratio.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09). Ceph documentation sources (ceph/ceph, doc/ directory, master).

Confirmed: `pveceph pool create <name> --erasure-coding k=..,m=..`, `<name>-data` and `<name>-metadata` pools, `--add_storages 0`, `data-pool` requirement, which options apply to the metadata pool, default `min_size` rule and the k+2 recommendation, the guide's two worked examples, profile changes needing a new pool, FastEC requirements; from Ceph: overhead (k+m)/k, at least k+m failure domains with k+m+1 advised, k > 8 discouraged, `allow_ec_overwrites`. Removed as unconfirmed: the node-count profile table, the recovery-network remark and the 'poor for databases' claim; `qm disk move` replaced by the documented `qm move-disk`.

Method: documentation only; no commands were run.
