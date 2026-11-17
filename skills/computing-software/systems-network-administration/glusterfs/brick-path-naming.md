---
id: computing-software.systems-network-administration.glusterfs.brick-path-naming
name: brick-path-naming
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, brick, naming, data-directory, mount-point]
level: practitioner
status: docs-checked
description: "GlusterFS brick naming convention: mount the filesystem at /data/glusterfs/VOLUME/BRICK and use a brick subdirectory so an unmounted brick fails to start."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Brick-Naming-Conventions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Brick path naming

Use the layout `/data/glusterfs/<volume>/<brick>/brick`. `/data` is suggested because FHS 2.3 does not clearly place shared server data under `/srv`.

- `<brick>` is the mount point of the brick filesystem.
- The actual brick is the `brick` subdirectory inside it. If the filesystem is not mounted, the brick fails to start.

One brick per server (run on every server, XFS-formatted `/dev/sdb1`):

```
mkdir -p /data/glusterfs/myvol1/brick1
mount /dev/sdb1 /data/glusterfs/myvol1/brick1
```

Then on one server only:

```
gluster volume create myvol1 replica 2 server{1..4}:/data/glusterfs/myvol1/brick1/brick
```

Two bricks per server: mount each disk at its own `brick1` and `brick2` directory. List every brick path explicitly in the create command. Writing `brick{1,2}` as one Bash brace expression expands the last braces first and pairs both bricks of a server together, so replicas would not span servers.

## Checked

2026-11-04: the layout, FHS 2.3 remark, one-brick and two-bricks-per-server examples, the fail-to-start benefit and the brace-expansion note were read against the glusterdocs page Brick-Naming-Conventions. Removed the claim about silently writing to the root disk, which the page does not state.

Method: documentation only; no commands were run.
