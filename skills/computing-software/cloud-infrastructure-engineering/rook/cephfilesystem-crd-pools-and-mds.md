---
id: computing-software.cloud-infrastructure-engineering.rook.cephfilesystem-crd-pools-and-mds
name: cephfilesystem-crd-pools-and-mds
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [cephfilesystem, metadatapool, datapools, activecount, activestandby, preservefilesystemondelete, mds-cache-memory-limit]
level: advanced
status: docs-checked
description: "CephFilesystem pool settings, naming rules, erasure-coded data pools, MDS activeCount and activeStandby, probes and MDS memory limits."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Shared-Filesystem/ceph-filesystem-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pools:
- `metadataPool` must use replication. `name` is optional.
- `dataPools` may be replicated or erasure coded (erasure coding needs bluestore OSDs). Multiple pools are added to the filesystem; assigning users or files to a pool is left to CephFS. Specifying `name` for each is highly recommended so spec changes do not make Rook lose the original pool order.
- For erasure coded data, create a replicated pool as the default data pool and the erasure coded one as a secondary pool. An EC 6+2 example needs at least three hosts and eight devices.
- Final pool names are `<fsName>-<poolName>` or `<fsName>-metadata`; set `preservePoolNames: true` to use names exactly as given.
- `preserveFilesystemOnDelete: true` keeps the filesystem if the CR is deleted accidentally (default false). It replaces the deprecated `preservePoolsOnDelete`.

Metadata server settings:
- `activeCount`: active MDS instances. Rook creates double that number, the extras standing by for failover.
- `activeStandby`: if true the extras keep a warm metadata cache in failover pairs; if false they are passive.
- `placement`, `annotations`, `labels`, `priorityClassName`, `resources`, `startupProbe` and `livenessProbe`.
- If a memory limit is set, Rook sets `mds_cache_memory_limit` from it. Rook recommends at least 4096MB for MDS daemons and logs a warning, but still runs the pod, if lower.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-filesystem-crd) against this skill: 19 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 1 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
