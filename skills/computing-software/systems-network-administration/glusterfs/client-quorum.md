---
id: computing-software.systems-network-administration.glusterfs.client-quorum
name: client-quorum
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, client-quorum, quorum-type, quorum-count, replica]
level: advanced
status: docs-checked
description: "Set GlusterFS client quorum with cluster.quorum-type (none, auto, fixed) and cluster.quorum-count, defaults for replica 3, and the ENOTCONN behaviour on quorum loss."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/arbiter-volumes-and-quorum.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Split-brain-and-ways-to-deal-with-it.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client quorum

Options: `cluster.quorum-type` and `cluster.quorum-count`.

```
gluster volume set <VOLNAME> cluster.quorum-type auto
gluster volume set <VOLNAME> cluster.quorum-type fixed
gluster volume set <VOLNAME> cluster.quorum-count 2
```

- `cluster.quorum-type` accepts `none` (default), `auto` or `fixed`.
- `auto`: writes allowed when at least ceil(bricks in replica / 2) are up. With an even replica count and exactly half up, the first brick must be among them.
- `fixed`: writes allowed when active bricks in the replica set are at least `cluster.quorum-count`. The count has no effect with `auto`.
- Replica 3 volumes have client quorum enabled and `auto` by default; leave it.
- Since GlusterFS 3.13, a replica subvolume that loses quorum becomes unavailable and operations fail with ENOTCONN instead of going read-only.
- Replica 2 volumes generally should not enable client quorum if high availability matters. With `fixed`, the count has to be two to prevent split-brain, otherwise a write can succeed on one brick and another write on the other.

See also server-quorum and create-arbiter-volume.

## Checked

2026-11-04: option names, none/auto/fixed semantics including the even-replica first-brick rule, the default of none, replica 3 defaulting to auto, the 3.13 ENOTCONN change and the replica 2 advice were read against the glusterdocs page arbiter-volumes-and-quorum. Reworded the replica 2 fixed-count line to match the page.

Method: documentation only; no commands were run.
