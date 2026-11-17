---
id: computing-software.systems-network-administration.glusterfs.peer-detach-server
name: peer-detach-server
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, peer-detach, peer-status, pool-list, trusted-pool]
level: intro
status: docs-checked
description: "Remove a server from a GlusterFS trusted storage pool with gluster peer detach, run from another pool member, and confirm with peer status."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Storage-Pools.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remove a server with peer detach

Run the command from a different server in the pool, not from the server being removed:

```
gluster peer detach <server>
```

Example (from server1, removing server4): `Detach successful`.

Confirm with:

```
gluster peer status
```

The detached server no longer appears and the `Number of Peers` count drops by one. `gluster pool list` shows the remaining pool including `localhost`.

## Checked

2026-11-04: detach command, running it from another pool member, `Detach successful`, and the peer count dropping from 3 to 2 were read against the glusterdocs page Storage-Pools. Removed the advice about bricks on the detached server, which the page does not cover.

Method: documentation only; no commands were run.
