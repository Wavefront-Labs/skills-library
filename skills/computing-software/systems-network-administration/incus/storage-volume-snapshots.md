---
id: computing-software.systems-network-administration.incus.storage-volume-snapshots
name: storage-volume-snapshots
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, storage-volume, volume-snapshot, snapshots-schedule, restore, expiry]
level: practitioner
status: docs-checked
description: "Snapshot custom Incus volumes: create with --reuse/--no-expiry, schedule with snapshots.schedule, restore in place or into a new volume with volume copy."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/storage_backup_volume.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volume snapshots

```
incus storage volume snapshot create <pool> <volume> [<snapshot>]
incus storage volume show <pool> <volume>/<snapshot>
incus storage volume edit <pool> <volume>/<snapshot>
incus storage volume snapshot delete <pool> <volume> <snapshot>
incus storage volume set <pool> <volume> snapshots.schedule=@daily
incus storage volume snapshot restore <pool> <volume> <snapshot>
incus storage volume copy <src_pool>/<src_vol>/<snap> <dst_pool>/<dst_vol>
```

- `--reuse` replaces a snapshot of the same name; `--no-expiry` keeps it despite a general expiry.
- Snapshots are kept forever unless `snapshots.expiry` is set. Also consider `snapshots.pattern`.
- Schedule accepts cron syntax such as `"0 6 * * *"`.
- Restore in place needs every instance using the volume stopped.
- `volume copy` from a snapshot restores into a new volume, including on another pool or remote.

## Checked

2026-11-04: confirmed against the Incus custom volume backup how-to (snapshot create/show/edit/delete/restore, `--reuse`, `--no-expiry`, `snapshots.schedule`, `snapshots.expiry`, `snapshots.pattern`, volume copy from a snapshot). Nothing removed.

Method: documentation only; no commands were run.
