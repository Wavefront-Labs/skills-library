---
id: computing-software.cloud-infrastructure-engineering.longhorn.snapshot-space-management
name: snapshot-space-management
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [snapshot-limits, snapshot-max-count, toomanysnapshots, snapshot-size, space]
level: advanced
status: docs-checked
description: "Cap Longhorn snapshot count and size with snapshot-max-count, SnapshotMaxCount, SnapshotMaxSize and the TooManySnapshots condition."
sources:
  - https://longhorn.io/docs/1.13.0/snapshots-and-backups/snapshot-space-management/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop snapshots from consuming unbounded space.

Per-volume snapshot count and size limits apply from v1.6.0. Removed snapshots, backing images and the volume head are excluded from both calculations. At the limit, delete snapshots before creating new ones.

Global settings:
- `snapshot-max-count`: 2 to 250, default 250; applies to new volumes only.
- `snapshot-count-warning-threshold`: 2 to 250, default 100; drives the `TooManySnapshots` condition.

Volume fields:
- `SnapshotMaxCount`: 0 or 2 to 250, default 0; non-zero values also cap the warning threshold.
- `SnapshotMaxSize`: 0 or greater than 2 x `Volume.Spec.Size`, default 0 (disabled). Expanding the volume raises it to 2 x size if smaller.

`TooManySnapshots` condition:
- Count threshold is `min(snapshot-count-warning-threshold, SnapshotMaxCount)`. With the default 100 and `SnapshotMaxCount` 50 the effective threshold is 50.
- Size threshold is active only when `SnapshotMaxSize` is non-zero and fires when total snapshot size reaches it.
- Both are checked independently each reconciliation; if both trip, the message lists each reason separated by a semicolon.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/snapshots-and-backups/snapshot-space-management/

No claim needed changing.

Method: documentation only; no commands were run.
