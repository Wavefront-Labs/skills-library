---
id: computing-software.database-administration.pgbackrest.pgbackrest-quick-start
name: pgbackrest-quick-start
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, backup, quick-start, stanza, postgresql]
level: intro
status: docs-checked
description: "Minimum sequence to protect a PostgreSQL cluster with pgBackRest: configure, archive, create stanza, check, backup."
sources:
  - https://pgbackrest.org/user-guide.html
  - https://pgbackrest.org/command.html
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get a first working backup and WAL archive.

Steps from the user guide:

1. Put a stanza section and a global section in the configuration file (default location /etc/pgbackrest/pgbackrest.conf).
2. Set `archive_command` and `archive_mode` in postgresql.conf, then restart PostgreSQL.
3. Create the stanza, then verify.
4. Take a backup.

```
[demo]
pg1-path=/path/to/pgdata

[global]
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
start-fast=y
```

```
# postgresql.conf
archive_command = 'pgbackrest --stanza=demo archive-push %p'
archive_mode = on
```

```
pgbackrest --stanza=demo stanza-create
pgbackrest --stanza=demo check
pgbackrest --stanza=demo backup
```

When no prior backup exists, the requested incr backup is automatically changed to full (a warning says so). Run commands as the user that owns the PostgreSQL data directory, usually postgres. Run `check` after `stanza-create` to prove both archiving and backup are configured correctly, and run `info` to see the result.

Retention starts with `repo1-retention-full`; see the retention skills. A backup also runs `expire` afterward when `expire-auto` is enabled (the default).

## Checked

2026-11-08: the Quick Start sequence, configuration layout, archive settings, incr-to-full warning and check advice confirmed in the User Guide; expire-auto default and the run-as-owner advice confirmed in the Command Reference and Configuration pages. Partial reads: the User Guide, Command Reference and Configuration pages are long, so only the sections relevant to this skill were read, not every page end to end.

Method: documentation only; no commands were run.
