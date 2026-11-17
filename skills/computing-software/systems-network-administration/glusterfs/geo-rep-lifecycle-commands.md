---
id: computing-software.systems-network-administration.glusterfs.geo-rep-lifecycle-commands
name: geo-rep-lifecycle-commands
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, geo-replication, lifecycle, reset-sync-time, status]
level: practitioner
status: docs-checked
description: "Start, stop, pause, resume and delete a GlusterFS geo-replication session, restart behaviour, reset-sync-time, status values and crawl states."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Geo-Replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Geo-replication session lifecycle

All forms use `gluster volume geo-replication <primary_volume> <secondary_user>@<secondary_host>::<secondary_volume>` followed by:

```
start [force]
stop [force]
pause
resume [force]
delete [force]
delete reset-sync-time
status [detail]
```

- Recreating a deleted session resumes where it stopped; use `delete reset-sync-time` to start over.
- `resume force` is used after a snapshot restore.
- `gluster volume geo-replication status` with no arguments shows all sessions.

STATUS values: Initializing (about a minute of checks), Created, Active (this node's gsyncd is syncing), Passive (standby, takes over if the Active fails), Faulty (check logs), Stopped.

CRAWL STATUS: Hybrid Crawl (initial sync or no changelogs), History Crawl (clears backlog after restart), Changelog Crawl (live).

`status detail` adds pending ENTRY, DATA and META counts, FAILURES and checkpoint columns.

## Checked

2026-11-04. Confirmed against the glusterdocs Geo-Replication page: start, stop, delete and status forms, pause and resume (snapshot section), delete reset-sync-time, resume force after restore, the STATUS and CRAWL STATUS values and the status detail columns. Nothing removed.

Method: documentation only; no commands were run.
