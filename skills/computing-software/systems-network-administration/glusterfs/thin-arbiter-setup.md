---
id: computing-software.systems-network-administration.glusterfs.thin-arbiter-setup
name: thin-arbiter-setup
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, thin-arbiter, replica-2, glustercli, quorum]
level: advanced
status: docs-checked
description: "Set up a GlusterFS thin-arbiter replica 2 volume: run the thin-arbiter glusterfsd process on a quorum node, then create the volume with glustercli --thin-arbiter."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Thin-Arbiter-Volumes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thin arbiter setup

1. On the quorum node, run the thin-arbiter process:

```
/usr/local/sbin/glusterfsd -N --volfile-id ta-vol -f /var/lib/glusterd/vols/thin-arbiter.vol --brick-port 24007 --xlator-option ta-vol-server.transport.socket.listen-port=24007
```

2. Create a replica 2 volume with the thin arbiter:

```
glustercli volume create <volname> --replica 2 <host1>:<brick1> <host2>:<brick2> --thin-arbiter <quorum-host>:<path-to-store-replica-id-file>
glustercli volume create testvol --replica 2 server{1..2}:/bricks/brick-{1..2} --thin-arbiter server-3:/bricks/brick_ta --force
```

The output says the volume must be started before data can be accessed.

Behaviour and caveats:

- The thin arbiter does no I/O; it is consulted only after the first failure, until healing completes.
- It can sit outside the trusted storage pool, even on a high-latency cloud host.
- Quorum is per brick, not per file: if any file on a data brick needs heal, that brick is treated as bad for all files.
- Reads fail with EIO when only one data brick is up.
- Each replica pair has its own replica-id file, created at mount time.

## Checked

2026-11-04: the glusterfsd command, the glustercli create syntax and example, and the behaviour bullets were read against the glusterdocs page Thin-Arbiter-Volumes. Nothing removed.

Method: documentation only; no commands were run.
