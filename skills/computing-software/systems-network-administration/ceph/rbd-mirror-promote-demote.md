---
id: computing-software.systems-network-administration.ceph.rbd-mirror-promote-demote
name: rbd-mirror-promote-demote
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, rbd, mirroring, promote, demote, failover, resync]
level: sme
status: docs-checked
description: "Fail over and fail back mirrored RBD images with demote, promote (including --force) and resync."
sources:
  - https://docs.ceph.com/en/latest/rbd/rbd-mirroring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Orderly failover: demote on the old primary, then promote on the other site.

```
rbd mirror image demote {pool-name}/{image-name}
rbd mirror pool demote {pool-name}
rbd mirror image promote {pool-name}/{image-name}
rbd mirror pool promote {pool-name}
```

If the old primary is unreachable, force the promotion on the surviving site:

```
rbd mirror image promote --force {pool-name}/{image-name}
rbd mirror pool promote --force {pool-name}
```

A forced promote can produce a split brain once the old site returns, because the two copies have diverged. Resolve it by demoting the stale image and asking it to resynchronise from the new primary:

```
rbd mirror image demote {pool-name}/{image-name}
rbd mirror image resync {pool-name}/{image-name}
```

Check outcome with `rbd mirror image status {pool-name}/{image-name}`. Stop the applications using the image before demoting.

Orderly failover means stop access to the primary image first (for example power down the VM or detach the drive), demote the current primary, promote the new one, then resume access on the alternate cluster. RBD supplies only the tools; an external mechanism must coordinate failover and failback. Forced promotion is for when demotion cannot propagate (cluster failure, outage) and produces split-brain until a resync is issued. The `rbd` resync command only flags the image; the local `rbd-mirror` daemon performs the resync asynchronously. For snapshot-based mirroring, resync copies contents only up to the most recent mirror snapshot, so create a new mirror snapshot on the primary to sync the latest changes.

## Checked

2026-11-09. Confirmed against: the Ceph RBD Mirroring page (docs.ceph.com/en/latest/rbd/rbd-mirroring/): Mirroring promotion and demotion, force promotion and split-brain, image resync and image status.

Removed: nothing; all commands and statements were found on the page.

Method: documentation only; no commands were run.

