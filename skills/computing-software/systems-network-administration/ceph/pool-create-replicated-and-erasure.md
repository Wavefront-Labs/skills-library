---
id: computing-software.systems-network-administration.ceph.pool-create-replicated-and-erasure
name: pool-create-replicated-and-erasure
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, pool, create, replicated, erasure-coding, pg-num]
level: practitioner
status: docs-checked
description: "Create replicated or erasure-coded Ceph pools with ceph osd pool create, including pg-num, CRUSH rule, profile and autoscale-mode arguments."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/pools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A pool name must be unique, and names beginning with `.` are reserved for Ceph internals. The two creation forms are:

```
ceph osd pool create {pool-name} [{pg-num} [{pgp-num}]] [replicated] \
         [crush-rule-name] [expected-num-objects]
ceph osd pool create {pool-name} [{pg-num} [{pgp-num}]] erasure \
         [erasure-code-profile] [crush-rule-name] [expected_num_objects] [--autoscale-mode=<on,off,warn>]
```

Points that matter:

- `pg-num` defaults to 32 (from `osd_pool_default_pg_num`), which the docs say is not suitable for most systems. With the autoscaler on, it adjusts the value afterwards.
- `pgp_num` should equal `pg_num`. Since Nautilus, Ceph scales `pgp_num` incrementally when `pg_num` changes, so you rarely set it.
- The CRUSH rule named must already exist or the command fails. Replicated pools default to the rule in `osd_pool_default_crush_rule`; erasure pools default to the `erasure-code` rule with the default profile, otherwise a rule named after the pool, created implicitly if absent.
- The erasure-code profile must exist. Changing the profile on a pool after creation has no effect; to change placement, point the pool at a different CRUSH rule built from the new profile.
- `expected-num-objects` makes PG splitting happen at creation, avoiding runtime split latency.
- `--bulk` creates a pool flagged `bulk`, which starts with a large number of PGs.

Every pool must then be tagged with an application before use.

## Checked

2026-11-03. Confirmed against: the Ceph Pools page (docs.ceph.com/en/latest/rados/operations/pools/): Creating a Pool; the Ceph Placement Groups page (docs.ceph.com/en/latest/rados/operations/placement-groups/): bulk.

Removed: nothing; the erasure default rule wording was corrected.

Method: documentation only; no commands were run.
