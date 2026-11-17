---
id: computing-software.database-administration.dragonfly.migrate-snapshot-restore
name: migrate-snapshot-restore
category: computing-software
field: database-administration
product: dragonfly
tags: [migration, rdb-import, snapshot-restore, dragonfly]
level: practitioner
status: docs-checked
description: "Move a Redis dataset into Dragonfly by loading an RDB file from the data directory at startup, accepting a downtime window."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/migrating-to-dragonfly/01-from-redis-instance/00-snapshot-and-restore.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Snapshot-based migration:

1. Create an RDB snapshot on Redis.
2. Copy the file into the directory Dragonfly will use as `dir`.
3. Start Dragonfly pointing at it:

```bash
./dragonfly --logtostderr --dir ./data --dbfilename dump
```

4. Repoint applications to Dragonfly.

The page warns the technique may involve a downtime window, and that synchronisation between the old Redis instance and the new Dragonfly instance might not be possible meanwhile, so plan and communicate the downtime.

Dragonfly recognises the RDB file in the `dir` path and loads it automatically during startup. The RDB file is named `dump.rdb`; `dir` is where snapshot files are loaded and saved, and `dbfilename` is the file name used for the database.

## Checked

2026-11-04. Confirmed against the Dragonfly Snapshot and Restore migration page (the cited migration/migrate-from-redis.md URL is now a 404, replaced): steps, the startup command, automatic loading, downtime note. Removed the near-zero-downtime replication pointer, which the page does not state and which cited a skill id that does not exist.

Method: documentation only; no commands were run.
