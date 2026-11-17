---
id: computing-software.systems-network-administration.ceph.pg-target-size-ratio
name: pg-target-size-ratio
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, placement-groups, target-size-ratio, target-size-bytes, autoscaler]
level: advanced
status: docs-checked
description: "Tell the Ceph PG autoscaler how much data each pool will hold using target_size_bytes and target_size_ratio to avoid later PG splits."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/placement-groups/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Without hints the autoscaler sizes pools by what they hold now, so a new, empty pool gets few PGs and is split later under load. Give it the expected final size instead.

Absolute size:

```
ceph osd pool set mypool target_size_bytes 100T
```

Relative share, against other pools that also have a ratio:

```
ceph osd pool set mypool target_size_ratio 1.0
```

If `mypool` has ratio 1.0 and one other pool also has ratio 1.0, each is expected to use 50% of cluster capacity. Several pools can be given shares that add up as you like:

```
ceph osd pool set data1 target_size_ratio 0.4
ceph osd pool set data2 target_size_ratio 0.3
ceph osd pool set data3 target_size_ratio 0.3
```

Rules:

- If both `target_size_bytes` and `target_size_ratio` are set for a pool, the ratio is used, `target_size_bytes` is ignored and the health check `POOL_HAS_TARGET_SIZE_BYTES_AND_RATIO` is raised.
- `ceph osd pool create` accepts `--target-size-bytes <bytes>` and `--target-size-ratio <ratio>`. Impossible target sizes (for example larger than the cluster) raise `POOL_TARGET_SIZE_BYTES_OVERCOMMITTED`.
- Ratios are normalised among the pools that have one, and capacity expected by pools with a target size is subtracted first (the EFFECTIVE RATIO column).
- Avoid setting both a BIAS other than 1.0 and a target ratio on the same pool (RGW index, CephFS metadata): use a higher bias for omap-rich pools and a target ratio for data-heavy pools.

Read the outcome in `ceph osd pool autoscale-status`.

## Checked

2026-11-03. Confirmed against: the Ceph Placement Groups page (docs.ceph.com/en/latest/rados/operations/placement-groups/): Specifying expected pool size, EFFECTIVE RATIO definition, BIAS.

Removed: nothing; two health check names and the create options were added from the page.

Method: documentation only; no commands were run.
