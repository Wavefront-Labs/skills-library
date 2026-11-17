---
id: computing-software.database-administration.pgbackrest.streaming-replication-standby
name: streaming-replication-standby
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, streaming-replication, primary-conninfo, standby, recovery-option]
level: advanced
status: docs-checked
description: "Add streaming replication to a pgBackRest-restored standby with primary_conninfo as a recovery-option."
sources:
  - https://pgbackrest.org/user-guide.html
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: cut standby lag by connecting directly to the primary.

Streaming applies changes as they are made instead of waiting for WAL archiving. Needed:

1. A replication-privileged role on the primary.
2. A `pg_hba.conf` entry for the standby's address with database `replication`, then a reload.
3. `primary_conninfo` supplied through pgBackRest.

```
[demo]
pg1-path=/path/to/pgdata
recovery-option=primary_conninfo=host=<primary-ip> port=5432 user=replicator
```

Use a `.pgpass` file (mode 600) for the password rather than putting it in primary_conninfo; it is more flexible and secure.

Restore the standby again with `--delta --type=standby restore`. The setting is written to `postgresql.auto.conf` beside `restore_command`. `--type=preserve` leaves an existing file in place.

The PostgreSQL log then shows `started streaming WAL from primary`. New tables created on the primary appear on the standby quickly, without `pg_switch_wal()`.

`archive-missing-retry=n` helps PostgreSQL see the end of archived WAL and switch to streaming; with the default, a steady stream of archived WAL keeps PostgreSQL reading from the archive.

## Checked

2026-11-08: the replication role, pg_hba.conf entry, primary_conninfo as recovery-option, .pgpass advice, --type=preserve and the streaming log line confirmed in the User Guide Streaming Replication section; archive-missing-retry behaviour confirmed in the Configuration page. Partial reads: the User Guide, Command Reference and Configuration pages are long, so only the sections relevant to this skill were read, not every page end to end.

Method: documentation only; no commands were run.
