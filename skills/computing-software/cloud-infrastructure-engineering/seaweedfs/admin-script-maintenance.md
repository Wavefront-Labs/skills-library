---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.admin-script-maintenance
name: admin-script-maintenance
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [vacuum, volume-fix-replication, admin-script, fix-replication]
level: advanced
status: docs-checked
description: "Run SeaweedFS cluster maintenance via the admin script plugin worker: default script, 17-minute interval, balance, vacuum and replication repair."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Volume-Management
  - https://github.com/seaweedfs/seaweedfs/wiki/Worker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# admin script maintenance

Maintenance scripts run in the `admin_script` plugin worker. Start:
```bash
weed admin -master=localhost:9333
weed worker -admin=localhost:12535
```
Built-in default script:
```
ec.balance -apply
fs.log.purge -daysAgo=7
volume.deleteEmpty -quietFor=24h -apply
volume.fix.replication -apply
s3.clean.uploads -timeAgo=24h
```
The script and its interval (default 17 minutes) are editable in the admin UI at `/plugin`.

Dedicated workers replaced some commands: `ec.encode` became `erasure_coding`, `volume.balance` became `volume_balance`. Job types of `weed worker`: `vacuum`, `volume_balance`, `admin_script` (default category) and `erasure_coding`, `iceberg_maintenance` (heavy). Select with `-jobType`; other options include `-heartbeat` (15s), `-maxDetect` (1), `-maxExecute` (4).

Legacy: `[master.maintenance]` in `master.toml` still exists as a fallback.

Missing replicas: a replicated volume with a missing replica becomes read-only until fixed by `volume.fix.replication`, which copies a healthy replica to restore the count.

Verify: the admin UI shows job runs; `volume.list` shows restored replicas.

## Checked

Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Volume Management (first 48 lines read: scripts, default script, fix missing volumes) and Worker (read in full).
