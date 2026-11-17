---
id: computing-software.systems-network-administration.glusterfs.peer-rejected
name: peer-rejected
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, peer-rejected, cksum, troubleshooting, glusterd]
level: advanced
status: docs-checked
description: "Fix common glusterd problems: Peer Rejected, accepted peer request, stale-lock 'Another transaction is in progress', and 'Transport endpoint is not connected'."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/troubleshooting-glusterd.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting glusterd

Logs: `/var/log/glusterfs/glusterd.log` and `cli.log`.

**Peer Rejected** (`gluster peer status` shows `State: Peer Rejected (Connected)`): glusterd.log has "Version of Cksums <vol-name> differ", meaning volume config is out of sync. Fix:

```
gluster volume get all cluster.max-op-version
gluster volume set all cluster.op-version <op-version>
```

**Accepted peer request**: later commands fail with "Host <hostname> is not in 'Peer in Cluster' state" because the handshake failed. Stop glusterd, set `state` to `3` in `/var/lib/glusterd/peers/<UUID>`, start glusterd.

**"Another transaction is in progress" / "Locking failed on <IP>"**: transient, retry later. For a stale lock, search glusterd.log for `lock being held by <uuid>`, match the UUID to a host with `gluster peer status`, and restart glusterd on that node.

**"Transport endpoint is not connected" with all bricks up**: a brick shut down unclean and glusterd holds a wrong port. Restart glusterd.

See op-version for the commands' background.

## Checked

2026-11-04: log paths, the four problem/solution pairs, the cksum message, the max-op-version and op-version commands and the `state` value 3 in the peers file were read against the glusterdocs page troubleshooting-glusterd. Nothing removed.

Method: documentation only; no commands were run.
