---
id: computing-software.systems-network-administration.glusterfs.rebalance-volume
name: rebalance-volume
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, rebalance, fix-layout, rebalance-status, force]
level: practitioner
status: docs-checked
description: "Rebalance a GlusterFS volume after adding bricks: fix-layout only, full rebalance with optional force, status checks, and stopping a run."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Managing-Volumes.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Logging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rebalance a volume

Fix layout only (no data moves; new files in existing directories can land on new bricks):

```
gluster volume rebalance <VOLNAME> fix-layout start
```

Fix layout and migrate existing data:

```
gluster volume rebalance <VOLNAME> start
gluster volume rebalance <VOLNAME> start force
```

By default rebalance skips moves that would leave the volume less balanced; this can leave link files behind that hurt performance. `force` overrides that.

Check progress and stop:

```
gluster volume rebalance <VOLNAME> status
gluster volume rebalance <VOLNAME> stop
```

Re-run `status` to confirm the scanned and rebalanced counts keep rising; completion shows status `completed`.

Since 3.6, file assignment takes brick size into account.

The rebalance log is `/var/log/glusterfs/VOLNAME-rebalance.log`.

## Checked

2026-11-04: fix-layout, full rebalance with and without force, the skipped-moves and link-file note, status and stop, the 3.6 brick-size note were read against the glusterdocs page Managing-Volumes (Rebalancing Volumes); the log path is on the Logging page. Nothing removed.

Method: documentation only; no commands were run.
