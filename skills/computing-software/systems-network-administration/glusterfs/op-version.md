---
id: computing-software.systems-network-administration.glusterfs.op-version
name: op-version
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, op-version, cluster-op-version, max-op-version, upgrade]
level: practitioner
status: docs-checked
description: "Check and raise the GlusterFS cluster op-version after an upgrade: get cluster.op-version and max-op-version, set the new value, and list client op-versions."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Upgrade-Guide/op-version.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster op-version

Current op-version (3.10 onwards) and the maximum the cluster supports:

```
gluster volume get all cluster.op-version
gluster volume get all cluster.max-op-version
```

Before 3.10 use `gluster volume get <VOLNAME> cluster.op-version`.

Raise it after upgrading (example for glusterfs 4.0.0):

```
gluster volume set all cluster.op-version 40000
```

List connected clients and their op-version info (3.10 onwards):

```
gluster volume status <all|VOLNAME> clients
```

Notes:

- Bumping the op-version is optional but advisable to use the latest features.
- The maximum is limited by the oldest upgraded nodes: if some nodes are at X and others newer, the maximum is X.
- A connected client that cannot support a feature you enable may need upgrading to the cluster op-version first.

Part of the post-upgrade steps in upgrade-online. A "Peer Rejected" state can also be fixed this way (see peer-rejected).

## Checked

2026-11-04: query commands and the 3.10 boundary, the max-op-version example, the 40000 value for glusterfs-4.0.0, the optional-but-advisable note and the client op-version query were read against the glusterdocs page Upgrade-Guide op-version. The Peer Rejected cross-reference is from the troubleshooting-glusterd page. Nothing removed.

Method: documentation only; no commands were run.
