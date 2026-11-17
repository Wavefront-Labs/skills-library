---
id: computing-software.systems-network-administration.glusterfs.create-distributed-volume
name: create-distributed-volume
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, distributed, volume-create, transport, no-redundancy]
level: intro
status: docs-checked
description: "Create a plain distributed GlusterFS volume with gluster volume create, including transport choice, any brick count, and the data-loss caveat."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Setting-Up-Volumes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a distributed volume

Syntax:

```
gluster volume create <NEW-VOLNAME> [transport tcp|rdma|tcp,rdma] <BRICKS>...
```

Example shape: `gluster volume create test-volume server1:/exp1 server2:/exp2`.

- Files are spread across the bricks; use it where redundancy is not important or is provided by other hardware or software layers.
- A disk or server failure can cause serious data loss, because directory contents are spread over the bricks.

After creating, the volume must be started before clients mount it (see start-volume-verify). Running `gluster volume info` should show `Type: Distribute`.

## Checked

2026-11-04: syntax, transport options, the data-loss note and `Type: Distribute` were read against the glusterdocs page Setting-Up-Volumes. Removed the claims that any brick count is allowed and that distributed is the default type, which the page does not state.

Method: documentation only; no commands were run.
