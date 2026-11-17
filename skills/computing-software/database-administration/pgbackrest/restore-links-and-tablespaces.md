---
id: computing-software.database-administration.pgbackrest.restore-links-and-tablespaces
name: restore-links-and-tablespaces
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, restore, link-map, tablespace-map, symlinks]
level: advanced
status: docs-checked
description: "Relocate symlinks and tablespaces during restore with link-all, link-map, tablespace-map and tablespace-map-all."
sources:
  - https://pgbackrest.org/command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restore onto a different storage layout.

By default symlinked directories and files are restored as normal directories and files in `$PGDATA`, because restoring symlinks to original destinations may be unsafe on another system.

- `--link-all`: restore all symlinks as they were on the source system.
- `--link-map=<name>=<path>`: change the destination of a particular symlink.
- `--tablespace-map=<name>=<path>`: move one tablespace. Tablespace locations are not stored in pg_tablespace, so moving is safe, though moving one into the data directory is not recommended.
- `--tablespace-map-all=<path>`: restore all tablespaces under a parent directory. Useful for development or staging systems with a different layout.

```
pgbackrest --stanza=demo --delta \
  --tablespace-map=ts_01=/path/to/ts_01 \
  --link-map=pg_wal=/path/to/wal restore
```

Tablespaces are restored to their original locations by default. Caution: tablespaces created after the backup started are not mapped by `tablespace-map-all`; take a new backup after creating a tablespace if mapping is needed.

Tablespace remapping is especially useful on replicas or upgraded systems whose mount points differ from the original host, as the option descriptions note.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest Command Reference (pgbackrest.org/command.html). Nothing needed removing. 

Method: documentation only; no commands were run.
