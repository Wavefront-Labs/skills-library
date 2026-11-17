---
id: computing-software.database-administration.dragonfly.snapshot-automatic-loading
name: snapshot-automatic-loading
category: computing-software
field: database-administration
product: dragonfly
tags: [automatic-loading, startup-load, restore, valkey-rdb, dragonfly]
level: practitioner
status: docs-checked
description: "How Dragonfly loads a snapshot at startup from dir, how to disable it, and loading RDB files written by Redis or Valkey."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/backups.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/migrating-to-dragonfly/01-from-redis-instance/00-snapshot-and-restore.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When a Dragonfly instance starts, it looks for a snapshot file in the configured `dir` path and loads it automatically.

- Disable this (and the automatic save on shutdown) by setting `dbfilename` to an empty value.
- With an S3 `dir`, Dragonfly loads the latest snapshot from the bucket on startup.
- Starting with Dragonfly v2.0.0, loading also accepts RDB files written by Valkey versions that use the `VALKEY080` header, including hash fields with per-field expiration.

To restore a Redis RDB, put it in `dir` and start with the matching name without extension:

```shell
./dragonfly --logtostderr --dir ./data --dbfilename dump
```

The migration page says this technique may involve a downtime window while applications are repointed to Dragonfly.

## Checked

2026-11-04. Confirmed against the Dragonfly Saving Backups page and the Snapshot and Restore migration page: automatic loading from `dir`, disabling via empty `dbfilename`, S3 loading, v2.0.0 Valkey `VALKEY080` header support, the startup command, downtime note. Nothing else removed.

Method: documentation only; no commands were run.
