---
id: computing-software.systems-network-administration.glusterfs.log-file-locations
name: log-file-locations
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, logs, glustershd-log, brick-log, glusterd-log]
level: intro
status: docs-checked
description: "Where GlusterFS writes logs under /var/log/glusterfs: glusterd, cli, bricks, self-heal daemon, rebalance, quota, NFS, FUSE mounts, geo-replication, plus Samba and Ganesha."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Logging.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/troubleshooting-afr.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log file locations

Under `/var/log/glusterfs/`:

- `glusterd.log`: management daemon, one per server.
- `cli.log`: the gluster CLI.
- `cmd_history.log`: commands run on a pool node.
- `bricks/<brick path>.log`: one per brick.
- `VOLNAME-rebalance.log`: one per volume.
- `glustershd.log`: self-heal daemon, one per server.
- `glfsheal-VOLNAME.log`: output of heal info and split-brain commands.
- `quotad.log`, `quota-crawl.log`, `quota-mount-VOLNAME.log`: quota daemon, crawl and auxiliary client.
- `nfs.log`: Gluster NFS.
- `<mountpoint path>.log`: each FUSE mount.
- `geo-replication/<primary>` and `geo-replication-secondary`: geo-replication.

Elsewhere:

- Samba: `/var/log/samba/glusterfs-VOLNAME-<ClientIP>.log`
- NFS-Ganesha: `/var/log/nfs-ganesha.log`

Raise detail with the client log level (default INFO; valid DEBUG, WARNING, ERROR, INFO, CRITICAL, NONE, TRACE):

```
gluster volume set $volname client-log-level $LEVEL
```

## Checked

2026-11-04: every log path, the per-server and per-volume counts, the Samba and Ganesha paths, and the client-log-level command, default and valid values were read against the glusterdocs pages Logging and troubleshooting-afr. Nothing removed.

Method: documentation only; no commands were run.
