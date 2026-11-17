---
id: computing-software.systems-network-administration.glusterfs.self-heal-commands
name: self-heal-commands
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, self-heal, heal-info, shd, replicate]
level: practitioner
status: docs-checked
description: "Trigger and inspect self-heal on replicate GlusterFS volumes: gluster volume heal, full, info variants, and how the self-heal daemon and index heal work."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Managing-Volumes.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Automatic-File-Replication.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/troubleshooting-afr.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Self-heal commands

The self-heal daemon (glustershd) runs on every node and crawls pending entries every `heal-timeout` seconds (by default every 10 minutes).

```
gluster volume heal <VOLNAME>          # index heal: files needing heal
gluster volume heal <VOLNAME> full     # crawl everything from root
gluster volume heal <VOLNAME> info     # list files needing heal
gluster volume heal <VOLNAME> info healed
gluster volume heal <VOLNAME> info failed
gluster volume heal <VOLNAME> info split-brain
```

How it works:

- Write transactions bump `trusted.afr.dirty` in pre-op and record failed bricks in `trusted.afr.<VOLNAME>-client-N` in post-op. The file's GFID is kept under `.glusterfs/indices/dirty` and `.glusterfs/indices/xattrop` on the brick.
- Inspect xattrs with `getfattr -d -m . -e hex <brick-path>/<file>`. A file is healthy when all AFR xattrs are zero or absent on every brick.
- Heal types are data, entry (directories) and metadata; each can have a different source brick.
- If AFR xattrs blame each other the file is in split-brain (see split-brain-detect).

Log: `/var/log/glusterfs/glustershd.log`.

## Checked

2026-11-04. Confirmed against the glusterdocs Managing Volumes, Automatic File Replication and Troubleshooting AFR pages: heal, heal full, and the info, info healed, info failed and info split-brain commands, the 10 minute daemon interval, dirty and pending xattrs, the indices directories, getfattr inspection, heal types and the glustershd.log path. Corrected: the page gives the 10 minute interval, not a figure of 600.

Method: documentation only; no commands were run.
