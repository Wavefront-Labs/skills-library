---
id: computing-software.systems-network-administration.glusterfs.create-replicated-volume
name: create-replicated-volume
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, replicated, replica, volume-create, force]
level: practitioner
status: docs-checked
description: "Create a replicated GlusterFS volume with gluster volume create replica N, keeping each replica on a different server and when force is needed."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Setting-Up-Volumes.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Quick-Start-Guide/Quickstart.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a replicated volume

Syntax:

```
gluster volume create <VOLNAME> replica <COUNT> [transport tcp|rdma|tcp,rdma] <BRICKS>...
```

Quick Start example, three copies on three servers:

```
gluster volume create gv0 replica 3 server1:/data/brick1/gv0 server2:/data/brick1/gv0 server3:/data/brick1/gv0
```

Rules:

- The number of bricks must equal the replica count.
- Put each brick on a different server. Creation fails if more than one brick of a replica set is on the same peer, unless you append `force`.
- Create the brick subdirectory (for example `mkdir -p /data/brick1/gv0`) on every server first.

Then start the volume (see start-volume-verify).

## Checked

2026-11-04: syntax, the bricks-equal-replica-count note, the same-peer failure with `force`, the replica 3 example and the per-server mkdir were read against the glusterdocs pages Setting-Up-Volumes and Quick-Start-Guide Quickstart. Removed the claim that several copies on one node would take the volume down, which the pages do not state.

Method: documentation only; no commands were run.
