---
id: computing-software.systems-network-administration.glusterfs.split-brain-cli-resolution
name: split-brain-cli-resolution
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, split-brain, bigger-file, latest-mtime, source-brick]
level: practitioner
status: docs-checked
description: "Resolve GlusterFS split-brain from the CLI with heal split-brain bigger-file, latest-mtime or source-brick, for one file or all files, and for GFID split-brain."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/resolving-splitbrain.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resolve split-brain from the CLI

Data and metadata split-brain:

```
gluster volume heal <VOLNAME> split-brain bigger-file <FILE>
gluster volume heal <VOLNAME> split-brain latest-mtime <FILE>
gluster volume heal <VOLNAME> split-brain source-brick <HOSTNAME:BRICKNAME> <FILE>
gluster volume heal <VOLNAME> split-brain source-brick <HOSTNAME:BRICKNAME>
```

- `<FILE>` is a path from the volume root, or a GFID string such as `gfid:<gfid-string>`.
- `bigger-file`: the larger replica copy is the source.
- `latest-mtime`: the copy with the latest modification time is the source.
- `source-brick` with a file: that brick is the source for that file. Without a file: every split-brain file on that brick is the source.

GFID split-brain uses the same three policies, with differences:

- `FILE` must be the absolute path from the mount point; GFIDs are not accepted.
- `source-brick` cannot resolve all GFID split-brains at once; run it per file.
- In distributed-replicated volumes, resolve directory GFID split-brain on every affected subvolume so all end with the same GFID.

Type-mismatch files fail with "Operation not permitted". Find affected files first (split-brain-detect).

## Checked

2026-11-04. Confirmed against the glusterdocs Resolving Split-brains page: the bigger-file, latest-mtime and source-brick command forms, file path or gfid:<gfid-string>, the GFID split-brain differences (absolute path, per-file source-brick, every subvolume in distributed-replicated volumes) and the Operation not permitted failure for type mismatches. Nothing removed.

Method: documentation only; no commands were run.
