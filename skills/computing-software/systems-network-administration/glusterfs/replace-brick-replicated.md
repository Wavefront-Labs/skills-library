---
id: computing-software.systems-network-administration.glusterfs.replace-brick-replicated
name: replace-brick-replicated
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, replace-brick, commit-force, brick-replacement, self-heal]
level: advanced
status: docs-checked
description: "Replace a failed or old brick in a replicate or distributed-replicate GlusterFS volume: mark the brick for heal via xattrs, run replace-brick commit force, and watch heal."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Managing-Volumes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replace a brick in a replicated volume

Steps from the guide (example volume `r2`, fuse mount `/mnt/r2`):

1. Confirm the new brick is empty and all other bricks are running. The brick being replaced may be down.
2. Find and stop the old brick process: `gluster volume status`, then `kill -15 <PID>`.
3. On the fuse mount, trigger pending self-heal metadata:

```
mkdir /mnt/r2/<name-of-nonexistent-dir>
rmdir /mnt/r2/<name-of-nonexistent-dir>
setfattr -n trusted.non-existent-key -v abc /mnt/r2
setfattr -x trusted.non-existent-key /mnt/r2
```

4. Check pending xattrs on a healthy brick: `getfattr -d -m. -e hex /path/to/r2_1` (your healthy brick path).
5. Confirm `/` needs healing: `gluster volume heal r2 info`.
6. Replace:

```
gluster volume replace-brick r2 Server1:/path/to/r2_0 Server1:/path/to/r2_5 commit force
```

7. `gluster volume status` should show the new brick online. Track `gluster volume heal r2 info`; pending changelog xattrs clear when heal finishes.

Only the `commit force` form of replace-brick is supported.

## Checked

2026-11-04: the seven steps, the setfattr trigger sequence, the getfattr and heal info checks, the `commit force` command and the only-variant-supported note were read against the glusterdocs page Managing-Volumes (Replacing bricks in Replicate/Distributed Replicate volumes). Nothing removed.

Method: documentation only; no commands were run.
