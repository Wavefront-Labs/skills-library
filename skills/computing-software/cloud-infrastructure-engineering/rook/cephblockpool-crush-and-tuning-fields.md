---
id: computing-software.cloud-infrastructure-engineering.rook.cephblockpool-crush-and-tuning-fields
name: cephblockpool-crush-and-tuning-fields
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [deviceclass, crushroot, enablecrushupdates, enablerbdstats, compression-mode, target-size-ratio, quotas]
level: advanced
status: docs-checked
description: "CephBlockPool tuning fields: deviceClass rules, crushRoot, pool name override, parameters, compression_mode, target_size_ratio and quotas."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Block-Storage/ceph-block-pool-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Placement and naming:
- `deviceClass`: restricts the pool's CRUSH rule to OSDs of that class. If set on any pool, set it on every pool, including the `.mgr` pool, otherwise Ceph warns about overlapping roots and the PG autoscaler and balancer can be confused.
- `crushRoot`: a custom CRUSH root; creating one needs the toolbox and Ceph tools.
- `enableCrushUpdates`: lets Rook update the pool CRUSH rule from the spec; default false, and a change can remap data.
- `replicasPerFailureDomain` (default 1) and `subFailureDomain` (default host) place several replicas per datacenter in stretched setups; with two datacenters and `size: 4`, set 2 per domain.
- `name`: overrides the pool name, supported only for `.nfs`, `.mgr`, `.nvmeof` and `.rgw.root`.
- `application`: defaults to rbd for CephBlockPool.

Other fields:
- `enableRBDStats`: per-volume IO statistics through dynamic OSD counters, default false; faster with object-map and fast-diff features.
- `parameters`: any pool property, for example `target_size_ratio` as a capacity hint for the PG autoscaler, or `compression_mode` with `none`, `passive`, `aggressive` or `force` (aggressive suits most cases).
- `quotas.maxSize` (a quantity string such as "10Gi") and `quotas.maxObjects`; 0 disables.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-block-pool-crd) against this skill: 23 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 2 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
