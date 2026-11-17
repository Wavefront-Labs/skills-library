---
id: computing-software.systems-network-administration.glusterfs.create-arbiter-volume
name: create-arbiter-volume
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, arbiter, replica, volume-create, split-brain]
level: practitioner
status: docs-checked
description: "Create an arbiter GlusterFS volume with replica 2 arbiter 1, where every third brick holds only metadata, and the older replica 3 arbiter 1 form."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/arbiter-volumes-and-quorum.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Setting-Up-Volumes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create an arbiter volume

An arbiter brick stores names and metadata only, so it prevents split-brain without a third full copy.

```
gluster volume create <VOLNAME> replica 2 arbiter 1 <NEW-BRICK> ...
```

Example with six servers:

```
gluster volume create testvol replica 2 arbiter 1 server{1..6}:/bricks/brick
```

- Every third brick in the list becomes an arbiter, so this creates two (2 + 1) replica subsets.
- The older syntax `replica 3 arbiter 1 host1:brick1 host2:brick2 host3:brick3` still works for backward compatibility.
- Creating an arbiter volume sets client quorum to `auto` automatically. Do not change it.
- Arbiter can be combined with distributed-replicate layouts.

Size the arbiter bricks with arbiter-brick-sizing. Start the volume afterwards (start-volume-verify).

## Checked

2026-11-04: the replica 2 arbiter 1 syntax, the six-server example, the n x (2 + 1) layout, the old replica 3 arbiter 1 form, metadata-only arbiter and the automatic client-quorum auto setting were read against the glusterdocs page arbiter-volumes-and-quorum; arbiter with distributed-replicate is on Setting-Up-Volumes. Nothing removed.

Method: documentation only; no commands were run.
