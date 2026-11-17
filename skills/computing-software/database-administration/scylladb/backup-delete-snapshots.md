---
id: computing-software.database-administration.scylladb.backup-delete-snapshots
name: backup-delete-snapshots
category: computing-software
field: database-administration
product: scylladb
tags: [snapshot, clearsnapshot, disk-space, housekeeping, backup]
level: practitioner
status: docs-checked
description: "Delete old ScyllaDB snapshots with nodetool clearsnapshot to reclaim disk: new snapshots never remove old ones, keyspace scoping, automate deletion and confirm the backup first."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/backup-restore/delete-snapshot.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Delete old snapshots

Taking a new snapshot does not delete the previous ones, and snapshots are hard links that pin SSTables after compaction replaces them. Old snapshots therefore consume disk steadily and must be removed.

```
nodetool clearsnapshot mykeyspace
```
Output: `Requested clearing snapshot(s) for [mykeyspace]`. It can be applied to one or several keyspaces; without arguments it clears all snapshots. Use `nodetool listsnapshots` first to see what exists and how much space each uses.

Rules:
- Confirm the data was copied to external storage before deleting.
- If snapshots are taken automatically (cron, Manager, scripted `nodetool snapshot`), delete the previous ones with an automated procedure as well, or use `--ttl` on `nodetool snapshot` so they expire by themselves.

`nodetool clearsnapshot -t <snapshot_name>` removes only the named snapshot.

## Checked

2026-11-04. Confirmed against delete-snapshot.rst, backup.rst, clearsnapshot.rst, listsnapshots.rst and snapshot.rst (--ttl): new snapshots do not delete old ones, output line, clearing all snapshots without arguments, -t tag. Removed the unsupported claims about incremental backup files and compacted snapshot sizes.

Method: documentation only; no commands were run.
