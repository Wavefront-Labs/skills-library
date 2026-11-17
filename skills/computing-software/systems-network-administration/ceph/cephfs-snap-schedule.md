---
id: computing-software.systems-network-administration.ceph.cephfs-snap-schedule
name: cephfs-snap-schedule
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephfs, snapshot, snap-schedule, retention, mgr]
level: practitioner
status: docs-checked
description: "Schedule CephFS snapshots with the snap_schedule mgr module and add retention policies."
sources:
  - https://docs.ceph.com/en/latest/cephfs/snap-schedule/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable the module and list state:

```
ceph mgr module enable snap_schedule
ceph fs snap-schedule status /
ceph fs snap-schedule list / --recursive=true
```

`status` prints all schedules and retention specs for a path; `list` prints schedules in a short single-line format. Both accept `--format=json`. All subcommands take an optional `fs` argument, and `--fs` is required when there is more than one file system.

Add a schedule: path, repeat interval, optional start time. The repeat interval is a number plus one of `h`, `d`, `w`, `M`, `y`. The start time defaults to last midnight, must be ISO8601, and is taken as UTC unless a zone is given.

```
ceph fs snap-schedule add / 1h
ceph fs snap-schedule add / 1h 11:55
```

Paths start at the CephFS root, not the host mount point: if the file system is mounted at `/mnt`, use `/some/path` for `/mnt/some/path`.

Retention keeps a number of snapshots at least a given period apart. One path has exactly one retention policy, which may hold several count-period pairs:

```
ceph fs snap-schedule retention add / h 24
ceph fs snap-schedule retention add / d 7
ceph fs snap-schedule retention remove / h 24
ceph fs snap-schedule retention add / 24h4w
```

The first line keeps 24 snapshots at least an hour apart and the second 7 at least a day apart. The period `n` keeps the last N snapshots regardless of timing (`10n`).

Remove schedules:

```
ceph fs snap-schedule remove / 1h 11:55
ceph fs snap-schedule remove / 1h
ceph fs snap-schedule remove /
```

The three forms remove one schedule, all schedules with that repeat interval, or all schedules on the path.

`activate` and `deactivate` (for example `ceph fs snap-schedule deactivate / 1d`) pause or resume schedules; a schedule whose directory is missing when due becomes inactive.

Limits stated by the page: retention per directory is capped by `mds_max_snaps_per_dir` (default 100, so by default at most 99 are retained), and the module itself keeps at most 50 snapshots per directory, shortening the retention list to the newest 50. A heavily loaded Manager can delay a snapshot slightly without drifting the schedule.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against "Snapshot Scheduling Module" on docs.ceph.com. Replaced the unsupported "snapshots accumulate until file system limits" with the limits the page states (the page gives both the 99 and 50 figures).
