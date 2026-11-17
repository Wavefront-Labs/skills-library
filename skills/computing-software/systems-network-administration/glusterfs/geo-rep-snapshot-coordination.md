---
id: computing-software.systems-network-administration.glusterfs.geo-rep-snapshot-coordination
name: geo-rep-snapshot-coordination
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, geo-replication, snapshot, pause, resume-force]
level: advanced
status: docs-checked
description: "Take consistent snapshots of both sides of a GlusterFS geo-replication pair: pause the session, snapshot with the same name, resume, and resume force after a restore."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Geo-Replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshots with geo-replication

Pause the session, snapshot both volumes with the same name, then resume:

```
gluster volume geo-replication <primary_volume> <secondary_user>@<secondary_host>::<secondary_volume> pause
gluster snapshot create <snapname> <volname>
gluster volume geo-replication <primary_volume> <secondary_user>@<secondary_host>::<secondary_volume> resume
```

Run the `snapshot create` on both the Primary and the Secondary volume.

After restoring snapshots, restart the session:

```
gluster snapshot restore <snapname>
gluster volume geo-replication <primary_volume> <secondary_user>@<secondary_host>::<secondary_volume> resume force
```

Caveat: snapshots of Primary and Secondary must not go out of order, and both volumes must be restored.

Snapshot prerequisites (thin LVM bricks) are in snapshot-create-manage.

## Checked

2026-11-04. Confirmed against the glusterdocs Geo-Replication page: pause, snapshot of both volumes with the same name, resume, and restore of both volumes followed by resume force. Nothing removed.

Method: documentation only; no commands were run.
