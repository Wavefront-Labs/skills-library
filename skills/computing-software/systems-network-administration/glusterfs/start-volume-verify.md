---
id: computing-software.systems-network-administration.glusterfs.start-volume-verify
name: start-volume-verify
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, volume-start, volume-info, mount-hang, status]
level: intro
status: docs-checked
description: "Start a GlusterFS volume after creation and confirm it with gluster volume info; an unstarted volume makes client operations hang after the mount."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Setting-Up-Volumes.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Quick-Start-Guide/Quickstart.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Start a volume and check it

A newly created volume is in the `Created` state. Start it before mounting; otherwise client operations after the mount hang.

```
gluster volume start <VOLNAME> [force]
gluster volume info
```

`gluster volume info` lists the volume name, type, status, brick count, transport and each brick. The status should read `Started` (the Quick Start confirms the volume shows "Started").

If it does not start, check `/var/log/glusterfs/glusterd.log` on one or all servers.

Quick Start smoke test: mount on a server with `mount -t glusterfs server1:/gv0 /mnt`, copy 100 files in, and check `ls -lA /mnt/copy* | wc -l` returns 100. On a replica 3 volume each brick directory should also hold 100 files.

## Checked

2026-11-04: the start command with force, the Created and Started states, the hang warning, the glusterd.log hint and the Quick Start smoke test were read against the glusterdocs pages Setting-Up-Volumes and Quick-Start-Guide Quickstart. Reworded the description, which said mounts fail where the page says client operations hang.

Method: documentation only; no commands were run.
