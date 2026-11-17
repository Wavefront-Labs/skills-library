---
id: computing-software.systems-network-administration.ceph.crush-weight-sets
name: crush-weight-sets
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, crush, weight-set, compat, per-pool, balancer]
level: sme
status: docs-checked
description: "Create and manage compat and per-pool CRUSH weight-sets, the mechanism behind balancer crush-compat mode."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/crush-map/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A weight-set is an alternative set of weights that CRUSH uses instead of the normal item weights. Two kinds exist.

The compat weight-set is a single set that older clients see as the real weights:

```
ceph osd crush weight-set create-compat
ceph osd crush weight-set reweight-compat {name} {weight}
ceph osd crush weight-set rm-compat
```

Per-pool weight-sets apply to one pool:

```
ceph osd crush weight-set create {pool-name} {mode}
ceph osd crush weight-set reweight {pool-name} {item-name} {weight [...]}
ceph osd crush weight-set ls
ceph osd crush weight-set rm {pool-name}
```

Use:

- You rarely edit these by hand. The balancer in `crush-compat` mode creates and adjusts the compat weight-set for you, keeping the normal weights equal to device size and nudging the weight-set up or down.
- `mode` for a per-pool set is `flat` (one weight for all devices or buckets) or `positional` (a different weight per position in the placement mapping). Per-pool weight sets need Luminous v12.2 or later on all servers and daemons.
- Use `ceph osd crush weight-set ls` before removing so you know which pools have one.

## Checked

2026-11-03. Confirmed against: the Ceph CRUSH Maps page (docs.ceph.com/en/latest/rados/operations/crush-map/): Creating a compat weight set, Creating per-pool weight sets; the Balancer page for crush-compat.

Removed: nothing; the mode values were added from the page.

Method: documentation only; no commands were run.
