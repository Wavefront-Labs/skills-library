---
id: computing-software.systems-network-administration.ceph.rbd-mirroring-pool-setup
name: rbd-mirroring-pool-setup
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, rbd, mirroring, peer, bootstrap, snapshot-based, journal]
level: advanced
status: docs-checked
description: "Set up RBD mirroring between two Ceph clusters with pool modes, peer bootstrap and mirror-snapshot schedules."
sources:
  - https://docs.ceph.com/en/latest/rbd/rbd-mirroring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two image modes exist: journal-based (uses the RBD journaling feature; every write is recorded in the journal first, so expect write latencies to nearly double) and snapshot-based (periodic mirror snapshots, replicating the delta).

Enable per pool in `image` or `pool` mode (or `init-only`):

```
rbd mirror pool enable [--site-name {local-site-name}] {pool-name} {mode}
```

Bootstrap peers: create a token on one site, import it on the other:

```
rbd mirror pool peer bootstrap create [--site-name {local-site-name}] {pool-name}
rbd mirror pool peer bootstrap import [--site-name {local-site-name}] [--direction {rx-only or rx-tx}] {pool-name} {token-path}
```

Use `rx-only` for one-way mirroring.

Per image:

```
rbd mirror image enable {pool-name}/{image-name} {mode}
rbd feature enable {pool-name}/{image-name} journaling
rbd mirror snapshot schedule add [--pool {pool-name}] [--image {image-name}] {interval} [{start-time}]
rbd mirror snapshot schedule status
rbd mirror image status {pool-name}/{image-name}
```

In `pool` mode, all images in the pool's default namespace with journaling enabled are mirrored; other namespaces must be configured separately.

Daemon placement: `rbd-mirror` pulls updates from the remote peer and applies them locally. For one-way replication it runs only on the secondary cluster, and for two-way on both. Each instance must reach both clusters' monitor and OSD hosts and the network needs enough bandwidth between sites. Journal-based mirroring needs Jewel or later and snapshot-based needs Octopus or later; journaling nearly doubles write latency. An alternative to bootstrap tokens creates a peer user with `ceph auth get-or-create client.rbd-mirror-peer mon 'profile rbd-mirror-peer' osd 'profile rbd'` and adds it with `rbd --cluster site-a mirror pool peer add image-pool client.rbd-mirror-peer@site-b`. Journal mode needs `exclusive-lock,journaling` features on the image; journaling depends on exclusive-lock.

## Checked

2026-11-09. Confirmed against: the Ceph RBD Mirroring page (docs.ceph.com/en/latest/rbd/rbd-mirroring/): the two modes, pool mode semantics, daemon placement, bootstrap and manual peer commands, image enable, journaling feature and snapshot schedules.

Removed: nothing; one pool-mode statement was narrowed to the default namespace.

Method: documentation only; no commands were run.

