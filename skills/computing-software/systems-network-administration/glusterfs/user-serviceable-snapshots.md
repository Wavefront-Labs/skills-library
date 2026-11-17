---
id: computing-software.systems-network-administration.glusterfs.user-serviceable-snapshots
name: user-serviceable-snapshots
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, uss, snaps-directory, snapshot, samba]
level: advanced
status: docs-checked
description: "Let users browse GlusterFS snapshots read-only through a hidden .snaps directory with features.uss, rename it, and expose it to Windows via Samba."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Managing-Snapshots.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User-serviceable snapshots (USS)

Enable per volume:

```
gluster volume set <volname> features.uss enable
```

- A hidden access directory (default `.snaps`) appears in every directory including the root.
- Snapshots are browsable read-only over FUSE, NFS or SMB.
- A snapshot must be activated before it shows up in `.snaps`.

Rename the directory:

```
gluster volume set <volname> snapshot-directory <new-name>
```

Windows Explorer access via Samba needs two things: the Samba `snapdir-entry-path` option (set when Samba loads GlusterFS, not a CLI setting) and:

```
gluster volume set <volname> features.show-snapshot-directory <on/off>
```

The default is off. With only `snapdir-entry-path` set, snapshots can still be reached by typing the path in the Run dialog but do not appear in Explorer. Explorer access works only from the root of the Samba share.

Activate snapshots with `gluster snapshot activate <snapname>` (see snapshot-create-manage).

## Checked

2026-11-04. Confirmed against the glusterdocs Managing Snapshots page: features.uss enable, the hidden .snaps default directory, read-only access over FUSE, NFS or SMB, the activation requirement, snapshot-directory, the Samba snapdir-entry-path option (not a volume set option), features.show-snapshot-directory default off, and the Run dialog versus Explorer behaviour and root-of-share limit. Nothing removed.

Method: documentation only; no commands were run.
