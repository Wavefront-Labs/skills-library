---
id: computing-software.systems-network-administration.ceph.pool-snapshots
name: pool-snapshots
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, pool, snapshot, mksnap, rmsnap, rados]
level: intro
status: docs-checked
description: "Create and remove pool-level snapshots in Ceph with ceph osd pool mksnap and rmsnap, and see where they differ from RBD and CephFS snapshots."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/pools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A pool snapshot captures the objects of an entire RADOS pool. Create and remove with:

```
ceph osd pool mksnap {pool-name} {snap-name}
ceph osd pool rmsnap {pool-name} {snap-name}
```

Things to know:

- Snapshots are one of the pool features the pools page lists.
Pool names beginning with `.` are reserved for Ceph's internal use, so do not choose them for your own pools. To see a pool's snapshots and other settings in one place, run `ceph osd pool ls detail`; to read one value, `ceph osd pool get {pool-name} {key}`; to list only names for scripts, `ceph osd pool ls`. Usage figures come from `rados df`, and I/O rates for one pool or all pools from `ceph osd pool stats [{pool-name}]`.

## Checked

2026-11-03. Confirmed against: the Ceph Pools page (docs.ceph.com/en/latest/rados/operations/pools/): Making and Removing a Snapshot of a Pool, List Pools, Showing Pool Statistics.

Removed: the rbd snap create and CephFS snapshot pointers and the retention/OSD data claims (not on the page).

Method: documentation only; no commands were run.
