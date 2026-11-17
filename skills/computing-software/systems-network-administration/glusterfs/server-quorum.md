---
id: computing-software.systems-network-administration.glusterfs.server-quorum
name: server-quorum
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, server-quorum, server-quorum-ratio, glusterd, quorum]
level: advanced
status: docs-checked
description: "Configure GlusterFS server-side quorum with cluster.server-quorum-type and cluster.server-quorum-ratio, ratio for two-node pools, and brick kill on quorum loss."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/arbiter-volumes-and-quorum.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server quorum

Options: `cluster.server-quorum-type` and `cluster.server-quorum-ratio`.

```
gluster volume set <VOLNAME> cluster.server-quorum-type server
gluster volume set <VOLNAME> cluster.server-quorum-ratio 51
```

- `cluster.server-quorum-type`: `none` or `server`. `server` makes the volume participate in server-side quorum.
- `cluster.server-quorum-ratio`: a percentage from 0 to 100. It is cluster-wide, so volumes in the same trusted pool cannot use different ratios.
- The page states no defaults for either option.
- For a two-node pool the ratio should be above 50%, so two separated nodes cannot both believe they have quorum.
- Adding a dummy node without bricks and setting 51% does not prevent split-brain.
- When server quorum is lost, glusterd kills the brick processes on the affected node, so even reads become impossible.

Client-side quorum is covered in client-quorum.

## Checked

2026-11-04: option names and values, the cluster-wide ratio, the above-50% advice for two-node pools, the dummy-node split-brain example and the brick kill on quorum loss were read against the glusterdocs page arbiter-volumes-and-quorum. The page shows option names only, not a set command, so the volume-set form is the general one.

Method: documentation only; no commands were run.
