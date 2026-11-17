---
id: computing-software.database-administration.pgbackrest.performance-tuning-checklist
name: performance-tuning-checklist
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, performance, tuning, zstd, async-archive]
level: sme
status: docs-checked
description: "Options that affect backup, restore and WAL archiving speed: compression, bundling, block incremental, process-max, async archiving, standby backup."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: speed up without guessing.

Options from the configuration reference that affect speed:

1. `compress-type=zst`: Zstandard compression; the default is `gz`, and `lz4` and `zst` are not available on all platforms.
2. `repo-bundle=y`: combines smaller files so fewer files are written to the repository, which is generally more efficient, especially on object stores such as S3.
3. `repo-block=y`: block incremental backup, which splits files into blocks backed up independently; `repo-bundle` must be enabled first.
4. `process-max`: default 1, allowed 1 to 999; do not set it so high that it hurts database performance.
5. `archive-async=y`: asynchronous `archive-push` and `archive-get`, which can reuse connections and use parallelism; see `spool-path`.
6. `backup-standby`: back up from a standby to reduce load on the primary; both primary and standby hosts must be configured.

```
[global]
compress-type=zst
repo1-bundle=y
repo1-block=y
process-max=4
archive-async=y
spool-path=/path/to/spool
backup-standby=prefer
```

Also see `buffer-size` (default 1MiB) and the repository storage options for object stores.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html). Removed: version-gate claims (since v2.xx), the backward-compatibility claim and the performance-tuning section paraphrase, which the fetched user guide does not contain. 

Method: documentation only; no commands were run.
