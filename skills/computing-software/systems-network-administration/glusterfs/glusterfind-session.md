---
id: computing-software.systems-network-administration.glusterfs.glusterfind-session
name: glusterfind-session
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, glusterfind, incremental, crawler, session]
level: practitioner
status: docs-checked
description: "List files changed on a GlusterFS volume with glusterfind: create a session, run pre with changelog or brickfind crawlers, mark progress with post, list and delete."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/GlusterFS-Tools/glusterfind.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# glusterfind sessions

```
glusterfind create SESSION_NAME VOLNAME [--force]
glusterfind pre SESSION_NAME VOLUME_NAME OUTFILE
glusterfind post SESSION_NAME VOLUME_NAME
glusterfind list [--session SESSION_NAME] [--volume VOLUME_NAME]
glusterfind delete SESSION_NAME VOLUME_NAME
```

- `create`: session name has no spaces. `--force` redistributes SSH keys, needed after adding a node to the volume. Session data lives in `$GLUSTERD_WORKDIR/glusterfind/SESSION_NAME/VOLNAME` (workdir default `/var/lib/glusterd`).
- `pre` writes changed paths (relative to the volume mount) to `OUTFILE`. Options: `--full` for a full find, `--crawler=changelog` (incremental only), `--crawler=brickfind` (full or incremental), `--file-prefix=/mnt/datavol/` to make paths absolute.
- `post` commits the time the last `pre` started as the starting point for the next run.
- `list` prints SESSION, VOLUME and SESSION TIME columns.

Caveats: deleted files are not listed (GFIDs cannot be mapped to paths once gone); renamed files show only the new name; all hardlinks are listed; files created before `build-pgfid` was enabled may fall back to a full crawl.

Example: `glusterfind create backup datavol`, then `glusterfind pre backup datavol /path/to/backup.txt`, then `glusterfind post backup datavol`.

## Checked

2026-11-04. Confirmed against the glusterdocs glusterfind page: command forms, session directory and default workdir, --force key redistribution, --full, --crawler=changelog and brickfind semantics, --file-prefix, post renaming status.pre, list columns, and the known issues (deleted, renamed, hardlinks) plus the build-pgfid full-crawl fallback. Removed: the claim that output has no change-type labels, which the page does not state.

Method: documentation only; no commands were run.
