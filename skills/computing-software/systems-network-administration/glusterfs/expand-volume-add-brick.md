---
id: computing-software.systems-network-administration.glusterfs.expand-volume-add-brick
name: expand-volume-add-brick
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, add-brick, expand, volume-expand, rebalance]
level: practitioner
status: docs-checked
description: "Expand a GlusterFS volume with gluster volume add-brick, probing new servers first, adding bricks in replica or disperse multiples, then rebalancing."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Managing-Volumes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expand a volume with add-brick

1. If the brick is on a new server, probe it into the pool:

```
gluster peer probe <SERVERNAME>
```

2. Add the brick:

```
gluster volume add-brick <VOLNAME> <NEW-BRICK>
```

3. Check the brick list:

```
gluster volume info <VOLNAME>
```

4. Rebalance so existing files reach the new brick (see rebalance-volume).

For distributed-replicated and distributed-dispersed volumes, add bricks in multiples of the replica or disperse count.

## Checked

2026-11-04: probe, add-brick, volume info, the rebalance step and the multiples rule were read against the glusterdocs page Managing-Volumes (Expanding Volumes). Nothing removed.

Method: documentation only; no commands were run.
