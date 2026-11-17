---
id: computing-software.database-administration.pgbackrest.upgrading-postgresql-major
name: upgrading-postgresql-major
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, upgrade, stanza-upgrade, pg-upgrade, major-version]
level: sme
status: docs-checked
description: "Re-point pgBackRest at the new cluster, run stanza-upgrade before starting it, and rebuild standbys."
sources:
  - https://pgbackrest.org/user-guide.html
  - https://pgbackrest.org/command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep backups working across a major upgrade.

Immediately after upgrading, set `pg-path` to the new location in every pgBackRest configuration, then run `stanza-upgrade`. Take a backup first. With multiple repositories the stanza is upgraded in each; use `--no-online` if the database is offline.

Sequence in the guide:

1. Stop the old primary and standby clusters.
2. Create the new cluster and run `pg_upgrade`.
3. Set `archive_command` and `archive_mode` in the new postgresql.conf, and update `pg1-path` on the primary, standby and repository host (and `pg2-path`).
4. Copy `pg_hba.conf`.
5. Run `stanza-upgrade` before starting the new cluster.
6. Start it and run `check`.
7. Remove the old cluster and create the new standby cluster.
8. Run a full backup (incr or diff is changed to full automatically) and restore the standby from it with `--type=standby`.
9. Re-enable `backup-standby` once the standby is restored.

```
pgbackrest --stanza=demo --no-online --log-level-console=info stanza-upgrade
```

A `check` from the repository host warns `unable to check pg2` while the standby is down, which is expected.

## Checked

2026-11-08: the upgrade sequence, stanza-upgrade, --no-online, the full-backup and standby restore steps and the expected pg2 warning confirmed in the User Guide Upgrading PostgreSQL section; stanza-upgrade behaviour confirmed in the Command Reference. Partial reads: the User Guide, Command Reference and Configuration pages are long, so only the sections relevant to this skill were read, not every page end to end.

Method: documentation only; no commands were run.
