---
id: computing-software.systems-network-administration.glusterfs.create-distributed-replicated-volume
name: create-distributed-replicated-volume
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, distributed-replicated, brick-order, replica-set, volume-create]
level: practitioner
status: docs-checked
description: "Create a distributed replicated GlusterFS volume: brick count as a multiple of the replica count and brick order so replica sets do not share a server."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Setting-Up-Volumes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a distributed replicated volume

```
gluster volume create <VOLNAME> replica <COUNT> [transport tcp|rdma|tcp,rdma] <BRICKS>...
```

- The brick count must be a multiple of the replica count.
- Brick order matters. Each consecutive group of `<COUNT>` bricks forms one replica set. List the first brick from every server, then the second brick from every server, and so on, so no replica set has two bricks on the same node.
- The same-peer restriction applies: creation fails when replicas share a server unless you add `force`.

Example idea: with replica 2 and four bricks listed as `server1:/exp1 server2:/exp2 server3:/exp3 server4:/exp4`, the sets are (server1, server2) and (server3, server4); files are distributed across the two sets.

Start the volume afterwards (start-volume-verify).

## Checked

2026-11-04: multiple-of-replica-count rule, consecutive-brick replica sets, the brick ordering advice and the same-peer failure with `force` were read against the glusterdocs page Setting-Up-Volumes. Removed the pointer about growing the volume, which the page does not cover.

Method: documentation only; no commands were run.
