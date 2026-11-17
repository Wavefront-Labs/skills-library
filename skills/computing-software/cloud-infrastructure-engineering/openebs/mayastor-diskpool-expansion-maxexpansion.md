---
id: computing-software.cloud-infrastructure-engineering.openebs.mayastor-diskpool-expansion-maxexpansion
name: mayastor-diskpool-expansion-maxexpansion
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [replicated-pv-mayastor, diskpool, expansion, maxexpansion, enospc, annotation, capacity]
level: advanced
status: docs-checked
description: "Grow a Mayastor DiskPool: set maxExpansion at creation, respect maxExpandableSize, expand the backing disk, then annotate the DiskPool or run kubectl openebs mayastor expand pool."
sources:
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/advanced-operations/diskpool-expansion
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
DiskPool expansion lets you add capacity before a pool fills, which avoids replicas failing with no-space (ENOSPC) errors. It is bounded: **each pool has a maximum expansion limit fixed at creation**, and pools created before this feature may have limited ability to grow.

**Configure the limit** with `maxExpansion` in the DiskPool CR, as either an absolute size in binary units (`800GiB`, `3.5TiB`, `1073741824B`) or a factor of the initial capacity (`1x`, `5x`, `20x`). `5x` allows growth to five times the initial size; the default is `1x`.

Two status fields track it:

- `maxExpandableSize`: the absolute size ceiling. Growing beyond it fails; it does not harm existing volumes or data but makes the extra capacity unusable.
- `diskCapacity`: the size of the underlying disk. `capacity` is the usable space after metadata reservation.

The disk can only grow by `maxExpandableSize - diskCapacity`.

**To expand:**

1. Grow the backing disk, without exceeding `maxExpandableSize`.
2. Trigger pool expansion either by annotating the CR with `kubectl annotate dsp <name> openebs.io/expand=true -n <ns>` (the operator removes the annotation on success or on an unrecoverable error), or with `kubectl openebs mayastor expand pool <pool-id> -n openebs`.
3. Confirm that both `capacity` and `diskCapacity` in the CR show the new size.

**Sizing advice from the page.** Prefer several DiskPools over over-expanding one: a large `maxExpansion` (for example taking a 100 GiB pool toward 50 to 60 TiB) reserves more metadata pages and can lengthen pool creation and import times. Large pools can still suit workloads with large volumes.

## Checked

2026-11-04. Confirmed against the DiskPool Expansion page: `maxExpansion` forms and the 1x default, `maxExpandableSize`, `diskCapacity`, the expansion limit formula, the annotation and plugin methods, and the sizing recommendation. Nothing removed.

Method: documentation only; no commands were run.
