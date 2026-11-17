---
id: computing-software.database-administration.dragonfly.manual-save-and-bgsave
name: manual-save-and-bgsave
category: computing-software
field: database-administration
product: dragonfly
tags: [save, bgsave, manual-backup, snapshot-formats, dragonfly]
level: practitioner
status: docs-checked
description: "Trigger Dragonfly snapshots manually with SAVE and BGSAVE, choose DF or RDB format, write to S3 or GCS, and know how BGSAVE differs from Redis."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/save.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/bgsave.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Syntax:

```
SAVE [RDB|DF] [cloud_uri] [filename]
BGSAVE [SCHEDULE] [RDB|DF] [cloud_uri] [filename]
```

`SAVE` produces a point-in-time snapshot as a set of DFS files; `SAVE RDB` writes an RDB file instead. The commands are `@admin`, `@slow`, `@dangerous`.

- `cloud_uri` writes to remote storage: `s3://` for S3 and `gs://` for GCP.
- `filename` overrides `dbfilename` for this save.

```shell
dragonfly> SAVE DF my_dump
dragonfly> SAVE DF s3://bucket/folder my_dump
```

`BGSAVE` is equivalent to `SAVE` and kept for compatibility. Differences from Redis:

- `SCHEDULE` is accepted but is a no-op. Concurrent saves are still rejected and saves are not queued.
- It replies a plain `OK`, not `Background saving started`.

## Checked

2026-11-04. Confirmed against the Dragonfly SAVE and BGSAVE command pages: both syntaxes, ACL categories, DFS files and `SAVE RDB`, `s3://` and `gs://` URIs, `filename` overriding `dbfilename`, the example commands, BGSAVE equivalent to SAVE, `SCHEDULE` a no-op, plain `OK` reply. Nothing removed.

Method: documentation only; no commands were run.
