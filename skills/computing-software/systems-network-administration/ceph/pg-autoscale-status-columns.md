---
id: computing-software.systems-network-administration.ceph.pg-autoscale-status-columns
name: pg-autoscale-status-columns
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, placement-groups, autoscale-status, target-ratio, bias, capacity]
level: practitioner
status: docs-checked
description: "Read ceph osd pool autoscale-status: what SIZE, RATE, RATIO, TARGET RATIO, BIAS, NEW PG_NUM and BULK mean and why output may be empty."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/placement-groups/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run `ceph osd pool autoscale-status` to see each pool, its relative utilisation and any recommended change.

Key columns:

- **SIZE** is data stored; **TARGET SIZE** is the amount you told Ceph to expect, and the larger of the two is used.
- **RATE** is the space amplification: 3.0 for three replicas, 1.5 for a k=4 m=2 erasure-coded pool.
- **RATIO** is (SIZE * RATE) / RAW CAPACITY, a fullness percentage. **FINAL RATIO** is the target PG utilisation.
- **TARGET RATIO** and **EFFECTIVE RATIO** show expected share relative to other pools that set a ratio. If both target size bytes and ratio are set, the ratio takes precedence.
- **BIAS** multiplies a pool's PG count. It matters for omap-heavy pools such as RGW index and CephFS metadata. When BIAS is not 1.0, leave the target ratio alone to avoid double-counting.
- **NEW PG_NUM** is always a power of two and appears only when it differs from the current value by more than the threshold.
- **BULK** shows whether the pool is flagged bulk.

If the command prints nothing, a pool probably spans several CRUSH roots, for example `.mgr` on the default root while other pools use device-class shadow trees. Constrain the spanning pool:

```
ceph osd pool set .mgr crush_rule replicated-ssd
```

This causes a small, usually quick backfill.

## Checked

2026-11-03. Confirmed against: the Ceph Placement Groups page (docs.ceph.com/en/latest/rados/operations/placement-groups/): autoscale-status column definitions, spanning-pool note and .mgr crush_rule example.

Removed: nothing.

Method: documentation only; no commands were run.
