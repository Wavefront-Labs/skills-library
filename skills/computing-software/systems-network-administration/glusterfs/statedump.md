---
id: computing-software.systems-network-administration.glusterfs.statedump
name: statedump
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, statedump, debugging, sigusr1, memory]
level: advanced
status: docs-checked
description: "Take GlusterFS statedumps of brick, NFS and client mount processes with gluster volume statedump or SIGUSR1, and find the dump directory and file names."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/statedump.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/troubleshooting-filelocks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Take statedumps

Find the output directory on a server node, and create it if missing:

```
gluster --print-statedumpdir
```

Brick processes (run on a server):

```
gluster volume statedump <volname>
```

Gluster NFS server:

```
gluster volume statedump <volname> nfs
```

Client mounts (on the client): send SIGUSR1 to the mount process:

```
kill -USR1 <pid-of-gluster-mount-process>
```

Files:

- Brick dumps: `hyphenated-brick-path.<pid>.dump.timestamp`.
- Other processes: `glusterdump.<pid>.dump.timestamp`.
- First and last lines hold start and end times in UTC.

The locks page notes dumps may go to `/tmp` or the directory set by the `server.statedump-path` volume option. `gluster volume statedump <VOLNAME> inode` dumps lock state.

Use dumps to debug hangs and growing memory: take several at regular intervals, or before and after the steps that raise memory use, and compare the allocation stats. For hangs, an xlator showing `complete=0` has not yet unwound its fop.

## Checked

2026-11-04. Confirmed against the glusterdocs Statedump and Troubleshooting File Locks pages: --print-statedumpdir, statedump for bricks and nfs, kill -USR1 for mounts, file naming, UTC first and last lines, the /tmp or server.statedump-path location, the inode argument, and the leak and hang debugging advice. Removed: the bug filing remark, which the pages do not state.

Method: documentation only; no commands were run.
