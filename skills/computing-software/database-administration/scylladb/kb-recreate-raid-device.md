---
id: computing-software.database-administration.scylladb.kb-recreate-raid-device
name: kb-recreate-raid-device
category: computing-software
field: database-administration
product: scylladb
tags: [raid, scylla-raid-setup, storage, xfs, disks]
level: practitioner
status: docs-checked
description: "Recreate the ScyllaDB RAID device without rerunning full setup using scylla_raid_setup --raiddev and --disks; storage is mounted, formatted and /var/lib/scylla created."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/raid-device.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Recreate RAID devices

During ScyllaDB setup a RAID device is created on all storage devices assigned to it. To redo only this step without the full setup phase (for example in a cloud with ephemeral storage, where a hard stop resets the devices and destroys the previous setup), run:

```
scylla_raid_setup --raiddev /dev/md0 --disks <comma-separated list of disks>
```
After it finishes the storage is mounted, formatted, and `/var/lib/scylla` is created.

## Checked

2026-11-04. Confirmed against kb/raid-device.rst: the scylla_raid_setup command line and the mounted, formatted, /var/lib/scylla outcome. Removed all cautions (data destruction, stopping the service, rerunning scylla_setup), which the page does not state.

Method: documentation only; no commands were run.
