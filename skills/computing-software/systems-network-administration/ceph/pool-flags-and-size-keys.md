---
id: computing-software.systems-network-administration.ceph.pool-flags-and-size-keys
name: pool-flags-and-size-keys
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, pool, size, min-size, nodelete, nopgchange, nosizechange, flags]
level: practitioner
status: docs-checked
description: "Use ceph osd pool set to tune replicas (size, min_size) and protective flags such as nodelete, nopgchange and nosizechange."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/pools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All pool attributes use the same form:

```
ceph osd pool set {pool-name} {key} {value}
ceph osd pool get {pool-name} {key}
```

Replica keys:

- `size`: number of replicas for objects in a replicated pool. Erasure-coded pools report a `size` of K+M that cannot be set directly.
- `min_size`: minimum number of active replicas (or shards) a PG needs to be active so I/O can proceed. For erasure-coded pools set it greater than K. `size` of 2 or `min_size` of 1 in production risks data loss.

Flags, set with `1` and cleared with `0`; each sets or unsets the matching NODELETE, NOPGCHANGE or NOSIZECHANGE flag on the pool:

- `nodelete`
- `nopgchange`
- `nosizechange`

```
ceph osd pool set data nosizechange 1
```

Other useful keys include `noscrub` and `nodeep-scrub` (disable scrubbing for the pool), `bulk`, `fast_read` for erasure-coded pools (read from all shards and decode with the first K replies, trading resources for latency), `recovery_priority` (range -10 to 10) and `recovery_op_priority`.

Per-pool scrub intervals `scrub_min_interval`, `scrub_max_interval` and `deep_scrub_interval` are in seconds; at the default of `0` the global `osd_*` values apply.

## Checked

2026-11-03. Confirmed against: the Ceph Pools page (docs.ceph.com/en/latest/rados/operations/pools/): Setting Pool Values, Setting the Number of RADOS Object Replicas.

Removed: what the three guard flags prevent (the page does not state it), and the closing advice.

Method: documentation only; no commands were run.
