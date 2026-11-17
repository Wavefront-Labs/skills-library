---
id: computing-software.systems-network-administration.glusterfs.gfid-to-path
name: gfid-to-path
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, gfid, aux-gfid-mount, build-pgfid, ancestry]
level: advanced
status: docs-checked
description: "Convert a GlusterFS GFID to a file path using the aux-gfid-mount option with glusterfs.ancestry.path (needs build-pgfid) or trusted.glusterfs.pathinfo."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/gfid-to-path.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GFID to path

A GFID is a cluster-unique UUID, similar to an inode number, stored in the `trusted.gfid` xattr.

Mount with the auxiliary GFID option:

```
mount -t glusterfs -o aux-gfid-mount vm1:test /mnt/testvol
```

Get a file's GFID string:

```
getfattr -n glusterfs.gfid.string /mnt/testvol/dir/file
```

Method 1: all paths, including hardlinks (separated by `:`), as seen from the mount point. Needs `build-pgfid` on first:

```
gluster volume set test build-pgfid on
getfattr -n glusterfs.ancestry.path -e text /mnt/testvol/.gfid/<GFID>
```

Method 2: the backend brick path (does not list all hardlinks):

```
getfattr -n trusted.glusterfs.pathinfo -e text /mnt/testvol/.gfid/<GFID>
```

## Checked

2026-11-04: the GFID description, the aux-gfid-mount mount, getfattr for the GFID string, both conversion methods and the build-pgfid step were read against the glusterdocs page Troubleshooting gfid-to-path. Removed the claim that files created before `build-pgfid` was enabled may not convert, which the page does not state.

Method: documentation only; no commands were run.
