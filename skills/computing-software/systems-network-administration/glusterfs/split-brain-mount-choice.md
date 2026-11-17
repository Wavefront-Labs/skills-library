---
id: computing-software.systems-network-administration.glusterfs.split-brain-mount-choice
name: split-brain-mount-choice
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, split-brain, split-brain-choice, heal-finalize, mount-point]
level: advanced
status: docs-checked
description: "Inspect and heal a GlusterFS data or metadata split-brain from a client mount using the replica.split-brain-status, split-brain-choice and heal-finalize virtual xattrs."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/resolving-splitbrain.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resolve split-brain from the mount point

Check status (data and metadata split-brain only; not GFID or directory split-brain):

```
getfattr -n replica.split-brain-status <path-to-file>
```

It reports the split-brain type and lists the choices (AFR children).

Pick a copy to read from, or clear the choice:

```
setfattr -n replica.split-brain-choice -v <choiceX> <path-to-file>
setfattr -n replica.split-brain-choice -v none <path-to-file>
```

Without a choice, reads fail with an input/output error.

Finalise the heal using the chosen copy:

```
setfattr -n replica.split-brain-heal-finalize -v <heal-choice> <path-to-file>
```

Caveats:

- If the `fopen-keep-cache` mount option is disabled, invalidate the inode before selecting a new choice: `setfattr -n inode-invalidate -v 0 <path-to-file>`.
- Does not work on NFS mounts, which lack xattr support.

## Checked

2026-11-04. Confirmed against the glusterdocs Resolving Split-brains page: replica.split-brain-status, split-brain-choice with none to clear, the input/output error without a choice, split-brain-heal-finalize, the fopen-keep-cache and inode-invalidate caveat, and the NFS limitation. Nothing removed.

Method: documentation only; no commands were run.
