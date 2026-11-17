---
id: computing-software.systems-network-administration.glusterfs.shrink-volume-remove-brick
name: shrink-volume-remove-brick
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, remove-brick, shrink, commit, data-migration]
level: practitioner
status: docs-checked
description: "Shrink a GlusterFS volume with remove-brick start, status and commit, migrating data off the brick first and observing the multiples-of-replica rule."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Managing-Volumes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shrink a volume with remove-brick

```
gluster volume remove-brick <VOLNAME> <BRICKNAME> start
gluster volume remove-brick <VOLNAME> <BRICKNAME> status
gluster volume remove-brick <VOLNAME> <BRICKNAME> commit
```

`start` triggers a rebalance that migrates data off the brick. Wait until `status` shows completed, then `commit`. Finally run `gluster volume info <VOLNAME>` to confirm the brick is gone.

Caveats:

- After commit, data left on the removed brick is not reachable through the Gluster mount; it stays on the brick and can be read directly. Copy any leftovers back in through a Gluster mount before reusing the brick.
- Committing can cause data loss and asks for confirmation.
- For replicated or dispersed layouts, remove bricks in multiples of the replica or stripe count, all from the same subvolume.

To replace a brick in a pure distribute volume, `add-brick` the new one first, then remove the old one with the same start, status and commit sequence.

## Checked

2026-11-04: the start, status and commit sequence, the automatic rebalance on start, the data-left-on-brick note, the confirmation prompt, the multiples and same-subvolume rule and the pure-distribute replacement were read against the glusterdocs page Managing-Volumes (Shrinking Volumes, Replace faulty brick). Nothing removed.

Method: documentation only; no commands were run.
