---
id: computing-software.systems-network-administration.glusterfs.create-dispersed-volume
name: create-dispersed-volume
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, dispersed, erasure-coding, redundancy, disperse]
level: advanced
status: docs-checked
description: "Create dispersed and distributed dispersed GlusterFS volumes: disperse and redundancy counts, minimum bricks, usable size formula and optimal stripe sizes."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Setting-Up-Volumes.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Quick-Start-Guide/Architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a dispersed volume

```
gluster volume create [disperse [<COUNT>]] [redundancy <COUNT>] [transport tcp|rdma|tcp,rdma] <BRICKS>...
```

Example: `gluster volume create test-volume disperse 3 redundancy 1 server1:/exp1 server2:/exp2 server3:/exp3`.

- At least 3 bricks. Redundancy must be greater than 0 and bricks must exceed 2 x redundancy; keep redundancy below half the brick count.
- Usable size = brick size x (number of bricks - redundancy).
- Use equal-capacity bricks in a disperse set.
- Combinations giving a power-of-two stripe size, 512 x (bricks - redundancy), perform best.
- If redundancy is omitted it is computed as the optimal value; a prompt is shown when that value is not 1, and if no optimal value exists it is assumed to be 1 with a prompt.
- More than one brick of a disperse set on the same server makes creation fail with a warning; `force` overrides it.

## Distributed dispersed

```
gluster volume create disperse <count> [redundancy <count>] ... <BRICKS>...
```

The `disperse` keyword and count are mandatory, and the total brick count must be a multiple of the disperse count. Bricks may share a node only if they belong to different subvolumes.

## Checked

2026-11-04: syntax, minimum of 3 bricks, redundancy rules, the usable-size formula, equal brick capacity, the 512 x (bricks - redundancy) stripe size, the automatic-redundancy prompts and the distributed dispersed rules were read against the glusterdocs page Setting-Up-Volumes. Reworded the automatic-redundancy and same-server lines to match the page.

Method: documentation only; no commands were run.
