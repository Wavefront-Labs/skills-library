---
id: computing-software.systems-network-administration.ceph.balancer-modes
name: balancer-modes
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, balancer, upmap, crush-compat, upmap-read, mgr]
level: practitioner
status: docs-checked
description: "Choose a Ceph balancer mode (upmap, crush-compat, read, upmap-read), check status and switch the module on or off."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/balancer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The mgr balancer module optimises PG placement across OSDs, automatically or under supervision.

```
ceph balancer status
ceph balancer off
ceph balancer mode crush-compat
ceph balancer mode upmap-read
```

Modes:

- **upmap** (default): stores explicit PG-to-OSD exceptions in the OSDMap. The result is nearly perfect, within one PG per OSD, but all clients must be Luminous or newer.
- **crush-compat**: maintains a compat weight-set, leaving the normal CRUSH weights equal to device size. It works with old clients, but cannot handle several CRUSH hierarchies with different rules that share OSDs.
- **read**: optimises read (primary) distribution only.
- **upmap-read**: upmap plus read balancing.

Limit to know: the balancer balances by PG shard count, not by bytes stored per PG. OSDs can look even by `ceph osd df` PGS column but still differ in used bytes, which makes a pool's `%USED` in `ceph df` exceed `%RAW USED`.

If the cluster is degraded the balancer makes no adjustments, with one exception: PGs stuck in `backfill_toofull` let the upmap and upmap-read balancers proceed.

Turn the balancer off before hand-managing upmap entries.

## Checked

2026-11-03. Confirmed against: the Ceph Balancer Module page (docs.ceph.com/en/latest/rados/operations/balancer/): Modes, Limitation, Throttling; the Ceph Using pg-upmap page (docs.ceph.com/en/latest/rados/operations/upmap/): turning the balancer off before custom entries.

Removed: nothing.

Method: documentation only; no commands were run.
