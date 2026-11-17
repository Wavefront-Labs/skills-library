---
id: computing-software.systems-network-administration.ceph.pg-num-min-max-bounds
name: pg-num-min-max-bounds
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, placement-groups, pg-num-min, pg-num-max, autoscaler]
level: advanced
status: docs-checked
description: "Bound the Ceph PG autoscaler for a pool with pg_num_min and pg_num_max so a mostly empty pool still has enough PGs for client I/O."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/placement-groups/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If a minimum is set, Ceph will not itself reduce (nor recommend reducing) `pg_num` below it, which sets a lower bound on client parallelism even when a pool is mostly empty. If a maximum is set, Ceph will not increase (nor recommend increasing) `pg_num` above it:

```
ceph osd pool set <pool-name> pg_num_min <num>
ceph osd pool set <pool-name> pg_num_max <num>
```

Use cases:

- `pg_num_min` for a pool that clients will hit hard immediately, so it does not sit at very few PGs.
- `pg_num_max` to stop the autoscaler growing a pool past a chosen count.
- `ceph osd pool create` also accepts `--pg-num-min <num>` and `--pg-num-max <num>`.

Related settings:

- The cluster-wide target is `mon_target_pg_per_osd` (default 100). The docs recommend 200 for all but the smallest deployments and warn that values above 500 may cause excessive peering traffic and RAM usage:

```
ceph config set global mon_target_pg_per_osd 200
```

- To preselect `pg_num` at creation, pass it to `ceph osd pool create {pool-name} [pg_num]`.

Check the effect with `ceph osd pool autoscale-status`.

## Checked

2026-11-03. Confirmed against: the Ceph Placement Groups page (docs.ceph.com/en/latest/rados/operations/placement-groups/): Specifying bounds on a pool's PGs, mon_target_pg_per_osd (default 100, 200 recommended, above 500 warning), Preselecting pg_num.

Removed: the use-case examples (VM image pool, metadata pool), which the page does not give.

Method: documentation only; no commands were run.
