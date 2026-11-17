---
id: computing-software.systems-network-administration.ceph.pg-bulk-flag
name: pg-bulk-flag
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, placement-groups, bulk, autoscaler, pool-create]
level: practitioner
status: docs-checked
description: "Start a large Ceph pool with a full complement of PGs by flagging it bulk, so performance does not suffer while the autoscaler scales up."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/placement-groups/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A pool flagged `bulk` is expected to be large. The autoscaler starts it with a full complement of PGs and scales down only if usage across the pool is uneven. Without the flag, the autoscaler starts small and grows the pool as data arrives, which can leave a big new pool underperforming at first.

Create a bulk pool:

```
ceph osd pool create <pool-name> --bulk
```

Set, unset or read the flag on an existing pool:

```
ceph osd pool set <pool-name> bulk <true/false/1/0>
ceph osd pool get <pool-name> bulk
```

`ceph osd pool autoscale-status` shows the flag in the BULK column. Small pools such as `.mgr` or metadata pools should stay non-bulk.

When to use it: data pools that you know will hold much of the cluster capacity, such as the main RBD or RGW data pool. For pools where you can estimate the size, combine bulk with `target_size_ratio` so the autoscaler also knows how much of the cluster each pool will take.

## Checked

2026-11-03. Confirmed against: the Ceph Placement Groups page (docs.ceph.com/en/latest/rados/operations/placement-groups/): Managing pools that are flagged with bulk.

Removed: nothing.

Method: documentation only; no commands were run.
