---
id: computing-software.systems-network-administration.glusterfs.peer-probe-server
name: peer-probe-server
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, peer-probe, trusted-pool, port-24007, storage-pool]
level: intro
status: docs-checked
description: "Add a server to a GlusterFS trusted storage pool with gluster peer probe, with the prerequisites (DNS, glusterd running, port 24007) and how to confirm the peer joined."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Storage-Pools.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Quick-Start-Guide/Quickstart.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Add a server with peer probe

Before probing:

- The server must be resolvable by hostname.
- glusterd must be running on the server being added.
- The firewall must allow port 24007.

Run the probe from a server that is already in the pool, not from the new server:

```
gluster peer probe <server>
```

Example output: `Probe successful`.

Check the result from the same server:

```
gluster peer status
```

Each peer should show `State: Peer in Cluster (Connected)`. The status lists only the other peers; `gluster pool list` also includes the local server (shown as `localhost`).

Each server starts as a pool of one until it is probed or probes others. Once a pool exists, only trusted members may probe new servers into it; a new server cannot probe the pool, it must be probed from the pool.

## Checked

2026-11-04: prerequisites (resolvable by hostname, glusterd running, port 24007), probe from a server already in the pool, `Probe successful`, `Peer in Cluster (Connected)` and the `gluster pool list` localhost entry were read against the glusterdocs page Storage-Pools (Managing Trusted Storage Pools); the only-trusted-members-may-probe note is on the Quick-Start-Guide Quickstart page. Nothing removed.

Method: documentation only; no commands were run.
