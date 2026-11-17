---
id: computing-software.systems-network-administration.zfs.zpool-raidz-expansion
name: zpool-raidz-expansion
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, raidz, expansion, raidz-expansion, attach, rewrite]
level: advanced
status: docs-checked
description: "Widen a RAID-Z vdev by attaching a disk with zpool attach, with the raidz_expansion feature, scratch space limits, parity ratio effects and zfs rewrite."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-attach.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RAID-Z expansion

Attaching a device to a RAID-Z group expands it:

```
zpool attach tank raidz2-0 sdg
```

(from a 6-wide to a 7-wide raidz2). It requires the `raidz_expansion` pool feature.

## How it works

Allocated data is read from the existing disks and rewritten across all disks including the new one. Progress shows in `zpool status`. Redundancy is maintained and fault tolerance is unchanged. If a disk fails mid-expansion, the expansion pauses until health is restored. Expansion can be repeated, and `-w` waits for it. A pool-wide scrub starts when it finishes to verify copied blocks.

## Constraints

- The new device must be at least as large as the smallest disk in the vdev.
- Each expansion uses the 3.5 MiB boot area as scratch space, which must hold one sector per disk; with ashift=16 that caps the vdev at 56 disks.
- The pool must not hold a checkpoint, since attach is prohibited while one exists.

## Parity ratio

Old blocks keep the original data-to-parity ratio; new blocks use the new one. To rewrite old blocks to the new ratio, use `zfs rewrite`. The vdev's assumed parity ratio does not change, so `zfs list` and `df` may report slightly less space than expected for new blocks.

Wait for it with `zpool wait -t raidz_expand tank`.

## Checked

2026-11-03. Pages read: zpool-attach(8), zpool-checkpoint(8), zpool-wait(8).

Confirmed: attach to raidz, raidz_expansion feature, progress, pause on disk failure, repeated expansion, -w, final scrub, 3.5 MiB scratch area and 56-disk figure at ashift=16, parity-ratio behaviour, zfs rewrite, and the checkpoint prohibition.

Method: documentation only; no commands were run.
