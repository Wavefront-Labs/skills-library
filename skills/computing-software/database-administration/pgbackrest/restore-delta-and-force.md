---
id: computing-software.database-administration.pgbackrest.restore-delta-and-force
name: restore-delta-and-force
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, restore, delta, force, sha-1]
level: practitioner
status: docs-checked
description: "Delta restore reuses matching files in a non-empty data directory; force changes how it compares."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restore faster than a full copy.

Plain restore needs an empty data directory. `--delta` instead decides which files can be kept and which must be restored. It uses checksums to decide which files in the data and tablespace directories can be kept.

```
pg_ctlcluster 17 demo stop
pgbackrest --stanza=demo --delta --log-level-console=detail restore
```

`--force` by itself forces PostgreSQL data and tablespace paths to be completely overwritten. Combined with `--delta` it uses a timestamp and size comparison instead of checksums.

Exclusions made at backup time (`--exclude`) are not honored: excluded files present in the target are removed on delta restore.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Command Reference (pgbackrest.org/command.html) and the pgBackRest Configuration Reference (pgbackrest.org/configuration.html). Removed: the SHA-1, global/pg_control removal, 'exists and matches backup' log text and process-max remarks, which are not on the fetched pages. 

Method: documentation only; no commands were run.
