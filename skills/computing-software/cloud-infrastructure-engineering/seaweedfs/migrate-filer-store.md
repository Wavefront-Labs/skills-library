---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.migrate-filer-store
name: migrate-filer-store
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [fs-meta-save, fs-meta-load, meta-backup, migrate]
level: advanced
status: docs-checked
description: "Move filer metadata between stores offline with fs.meta.save/load or online with weed filer.meta.backup; file content never moves."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Migrate-Between-Filer-Stores
  - https://github.com/seaweedfs/seaweedfs/wiki/Async-Filer-Metadata-Backup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# migrate filer store

Only metadata moves; chunks stay on volume servers.

Option 1, offline (works between any stores, needs a short write stop):
```
weed shell
> fs.meta.save -o backup.meta.gz /
(stop filer, edit filer.toml to the new store, start filer)
> fs.meta.load -concurrency=8 backup.meta.gz
> fs.ls -l /
> fs.verify /
```
Use `-concurrency=1` for stores such as Redis. `-dirPrefix=/buckets/important` loads only a subtree. The saved file doubles as a rollback backup.

Option 2, online:
```bash
weed filer.meta.backup -config=/path/to/backup_filer.toml -filer=localhost:8888
```
`backup_filer.toml` enables the new store like `filer.toml`. The first run walks all metadata, then streams changes; progress is checkpointed in the target store so you can stop and resume (`-restart` forces a full run). When the log shows it has caught up: briefly stop writes, point `filer.toml` at the new store, restart the filer, resume writes.

The backup store may differ from the source (e.g. LevelDB backing up Redis).

Verify: compare `fs.ls` output and run `fs.verify` before cutting over.

## Checked
Checked 2026-11-09: metadata-only migration, the offline save/load sequence with `-concurrency` and `-dirPrefix`, the Redis caveat, the online `filer.meta.backup` command with checkpointing, `-restart` and cutover steps, and the different-backup-store note all match both pages. Nothing removed.
Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Migrate-Between-Filer-Stores and Async-Filer-Metadata-Backup, both read in full from a local clone of the wiki.
