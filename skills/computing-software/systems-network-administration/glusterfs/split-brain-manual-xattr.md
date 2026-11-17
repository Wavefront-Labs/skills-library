---
id: computing-software.systems-network-administration.glusterfs.split-brain-manual-xattr
name: split-brain-manual-xattr
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, split-brain, getfattr, setfattr, changelog]
level: sme
status: docs-checked
description: "Resolve GlusterFS split-brain manually by reading trusted.afr changelog xattrs with getfattr, resetting the bad copy with setfattr, and triggering heal with ls -l."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/resolving-splitbrain.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manual split-brain resolution with xattrs

1. Get the split-brain file path (split-brain-detect).
2. Close applications using the file on the mount; power off VMs.
3. Read the changelogs on each brick:

```
getfattr -d -m . -e hex <file-path-on-brick>
```

`trusted.afr.<volname>-client-<N>` holds changelogs. Each value is 24 hex digits: first 8 data, next 8 metadata, last 8 directory entries. `N` is the brick's position in `gluster volume info` minus one.

4. Decide the good copy, then reset the bad copy's changelog:

```
setfattr -n <attribute-name> -v <attribute-value> <file-path-on-brick>
setfattr -n trusted.afr.vol-client-0 -v 0x000000000000000100000000 /gfs/brick-b/a
```

5. Trigger heal: `ls -l <file-path-on-gluster-mount>`.

Notes:

- Data and metadata split-brain may need fixing on different bricks.
- Directory entry split-brain: names that differ are merged; if the same name has different GFIDs, remove the conflicting file from one brick together with its gfid-link `<brick>/.glusterfs/<xx>/<yy>/<gfid>`. Check for and delete hard links to that file first.

## Checked

2026-11-04. Confirmed against the glusterdocs Resolving Split-brains page: getfattr and setfattr commands, the trusted.afr changelog layout of data, metadata and entry counts, the client index rule, the example value, ls -l to trigger heal, and the directory entry split-brain handling with the gfid-link removal. Nothing removed.

Method: documentation only; no commands were run.
