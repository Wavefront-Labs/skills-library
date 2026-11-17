---
id: computing-software.systems-network-administration.glusterfs.snapshot-config-limits
name: snapshot-config-limits
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, snapshot, snap-max-hard-limit, auto-delete, activate-on-create]
level: practitioner
status: docs-checked
description: "Configure GlusterFS snapshot limits with snapshot config: snap-max-hard-limit, snap-max-soft-limit, auto-delete and activate-on-create, and how each behaves."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Managing-Snapshots.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot config and limits

```
gluster snapshot config [volname] ([snap-max-hard-limit <count>] [snap-max-soft-limit <percent>])
                                  | ([auto-delete <enable|disable>])
                                  | ([activate-on-create <enable|disable>])
```

Without keywords it shows config for all volumes; with a volname it shows that volume's values.

- `snap-max-soft-limit` and `auto-delete` are global and cannot be set per volume.
- The system-wide limit takes precedence over volume-specific limits.
- At the soft limit: with `auto-delete` enabled each successful creation deletes the oldest snapshot; disabled, each creation issues a warning.
- At the hard limit, new snapshot creation is refused.
- `activate-on-create` is disabled by default; when enabled, new snapshots are activated at creation.

Snapshot commands are in snapshot-create-manage.

## Checked

2026-11-04. Confirmed against the glusterdocs Managing Snapshots page: the snapshot config syntax, global soft limit and auto-delete, system limit precedence, soft-limit and hard-limit behaviour, and activate-on-create default. Nothing removed.

Method: documentation only; no commands were run.
