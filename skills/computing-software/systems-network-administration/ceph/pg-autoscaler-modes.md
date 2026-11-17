---
id: computing-software.systems-network-administration.ceph.pg-autoscaler-modes
name: pg-autoscaler-modes
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, placement-groups, pg-autoscaler, pg-autoscale-mode, noautoscale]
level: practitioner
status: docs-checked
description: "Control Ceph PG autoscaling per pool with pg_autoscale_mode (on, warn, off), the cluster default and the noautoscale flag."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/placement-groups/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each pool has a `pg_autoscale_mode` property:

- `off`: you choose `pg_num` yourself
- `on`: the cluster adjusts the PG count automatically
- `warn`: a health check is raised when the count needs adjusting

```
ceph osd pool set foo pg_autoscale_mode on
```

For pools created after initial setup, change the default:

```
ceph config set global osd_pool_default_pg_autoscale_mode <mode>
```

The autoscaler can be paused or resumed for all pools at once with the `noautoscale` flag, which is off by default:

```
ceph osd pool set noautoscale
ceph osd pool unset noautoscale
ceph osd pool get noautoscale
```


The autoscaler is conservative. It only acts when current `pg_num` differs from its recommendation by more than a threshold factor (default factor 3 for scaling down; the threshold is lowered automatically when scaling up to a large recommended count). Change the factor with `ceph osd pool set threshold 2.0` and read it with `ceph osd pool get threshold`.

## Checked

2026-11-03. Confirmed against: the Ceph Placement Groups page (docs.ceph.com/en/latest/rados/operations/placement-groups/): pg_autoscale_mode values, osd_pool_default_pg_autoscale_mode, noautoscale, threshold.

Removed: the claim that cephadm upgrade toggles noautoscale, and the advice on which mode to start with (not in the page).

Method: documentation only; no commands were run.
