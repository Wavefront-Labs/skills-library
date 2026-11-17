---
id: computing-software.database-administration.pgbackrest.restore-selected-databases
name: restore-selected-databases
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, restore, db-include, db-exclude, sparse-files]
level: advanced
status: docs-checked
description: "Restore only chosen databases; the rest become sparse zeroed files that must be dropped afterward."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restore part of a cluster to save space or time.

`--db-include` (repeatable) restores only the named databases. Everything else is restored as sparse, zeroed files so PostgreSQL can still perform recovery. Built-in databases (template0, template1, postgres) are always restored. `--db-exclude` (repeatable) restores all but the named databases; used with `--db-include` it applies only to the standard system databases.

```
pgbackrest --stanza=demo --delta --db-include=test2 restore
```

After recovery the databases that were not restored are not accessible but can be removed with `drop database`. The command reference points to the Restore Selected Databases section of the user guide for further information and caveats.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest Command Reference (pgbackrest.org/command.html). Removed: the --type=immediate caveat, ignore_invalid_pages, the 'relation mapping file' error text, the size figures and the info database list output, none of which are on the fetched pages. 

Method: documentation only; no commands were run.
