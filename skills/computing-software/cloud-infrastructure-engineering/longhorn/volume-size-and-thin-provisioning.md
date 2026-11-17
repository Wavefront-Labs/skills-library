---
id: computing-software.cloud-infrastructure-engineering.longhorn.volume-size-and-thin-provisioning
name: volume-size-and-thin-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [volume-size, actual-size, thin-provisioning, snapshots, space-estimate]
level: practitioner
status: docs-checked
description: "Longhorn nominal versus actual volume size, why deleting files does not shrink replicas, and the (N+1) times average snapshot size estimate."
sources:
  - https://longhorn.io/docs/1.13.0/nodes-and-volumes/volumes/volume-size/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: predict real disk consumption.

Nominal size: set at creation; the space available to the volume. Each replica is a sparse file that can grow up to it. Replicas schedule only on nodes with enough allocatable space to cover it. The maximum depends on the filesystem (16383 GiB for ext4).

Actual size: the space each replica uses on its node, including the volume head and all snapshots. It can exceed the nominal size because snapshot data counts. The UI shows it only while the volume is running.

Thin provisioning behaviour:
- Actual size grows as blocks are written.
- Deleting files does not shrink it; Longhorn does not automatically issue TRIM or UNMAP, so use filesystem trim manually.
- Rewriting freed space may not reuse blocks, so actual size can reach or pass the nominal size.
- Deleting snapshots (purge or coalescing) can shrink it; the example volume went from 16.2 Gi to 11.4 Gi after deleting snapshot#1.
- Snapshot cleanup temporarily needs extra space, up to the nominal size.

Estimate: maximum consumption is roughly (N + 1) x the average head or snapshot actual size, where N counts snapshots including the volume head; the +1 covers temporary space for snapshot deletion.

A full volume means its filesystem is at 100% and writes fail with "no space left on device". A full node disk can also fail writes and block volume operations even if the volume has free space.

## Checked

2026-11-08. Read in full against https://longhorn.io/docs/1.13.0/nodes-and-volumes/volumes/volume-size/ : nominal and actual size, TRIM behaviour, the (N + 1) estimate, example 16.2 Gi to 11.4 Gi, no-space troubleshooting. Nothing else was removed.

Method: documentation only; no commands were run.
