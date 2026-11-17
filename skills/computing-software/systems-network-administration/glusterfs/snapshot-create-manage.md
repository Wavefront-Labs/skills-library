---
id: computing-software.systems-network-administration.glusterfs.snapshot-create-manage
name: snapshot-create-manage
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, snapshot, snapshot-create, thin-lvm, restore]
level: practitioner
status: docs-checked
description: "Create, list, inspect, activate, deactivate, delete and restore GlusterFS volume snapshots, with the thin-LVM prerequisites and offline-restore rule."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Managing-Snapshots.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create and manage snapshots

Prerequisites: GlusterFS 3.6 or later; each brick on its own independent thinly provisioned LVM holding only brick data; no brick on thick LVM (see brick-lvm-thin-pool).

```
gluster snapshot create <snapname> <volname> [no-timestamp] [description <description>]
gluster snapshot list [volname]
gluster snapshot info [(snapname | volume <volname>)]
gluster snapshot status [(snapname | volume <volname>)]
gluster snapshot activate <snapname>
gluster snapshot deactivate <snapname>
gluster snapshot delete (all | <snapname> | volume <volname>)
gluster snapshot restore <snapname>
```

- A timestamp is appended to the name unless `no-timestamp` is given. Descriptions are limited to 1024 characters.
- The volume must exist and be started, with all bricks online.
- Snapshots are not activated by default.
- `delete all` removes every snapshot on the system.
- Restore is offline: it fails if the volume is started. A restored snapshot disappears from the list.

Limits and auto-delete are in snapshot-config-limits.

## Checked

2026-11-04. Confirmed against the glusterdocs Managing Snapshots page: prerequisites (3.6 or later, independent thin LVM, no thick LVM), all command forms, timestamp and no-timestamp, 1024 character description limit, started volume with bricks online, no activation by default, delete all, and the offline restore rule. Nothing removed.

Method: documentation only; no commands were run.
