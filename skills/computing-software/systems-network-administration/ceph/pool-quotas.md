---
id: computing-software.systems-network-administration.ceph.pool-quotas
name: pool-quotas
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, pool, quota, max-bytes, max-objects, capacity]
level: practitioner
status: docs-checked
description: "Cap a Ceph pool by bytes or object count with ceph osd pool set-quota, and remove the cap by setting it to zero."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/pools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Quotas limit the maximum number of bytes or RADOS objects in a pool. Set either one or both:

```
ceph osd pool set-quota {pool-name} [max_objects {obj-count}] [max_bytes {bytes}]
ceph osd pool set-quota data max_objects 10000
```

To remove a quota, set its value to `0`:

```
ceph osd pool set-quota data max_objects 0
```

Usage notes:

- A quota can apply to bytes only, objects only, or both.
- Pool utilisation comes from `rados df`; I/O for one pool or all pools comes from `ceph osd pool stats [{pool-name}]`.
- The `POOL_NEAR_FULL` and `POOL_FULL` health checks relate to pool quotas: pools at or near quota raise them (thresholds `mon_pool_quota_warn_threshold` and `mon_pool_quota_crit_threshold`), and `POOL_FULL` means writes are no longer allowed.

## Checked

2026-11-03. Confirmed against: the Ceph Pools page (docs.ceph.com/en/latest/rados/operations/pools/) and the Health checks page (docs.ceph.com/en/latest/rados/operations/health-checks/): POOL_FULL, POOL_NEAR_FULL.

Removed: the replica-multiplication claim, ceph df detail usage claim and the CephFS/RGW quota pointers.

Method: documentation only; no commands were run.
