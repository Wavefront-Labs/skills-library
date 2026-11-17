---
id: computing-software.database-administration.pgbackrest.restore-basics
name: restore-basics
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, restore, backup-set, delta, recovery]
level: intro
status: docs-checked
description: "Restore the latest backup from the first repository holding backups, or pick one with --set and --repo."
sources:
  - https://pgbackrest.org/command.html
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restore a cluster safely.

The cluster must be stopped. Without `--delta`, all files must be removed from the data directory first. `restore` selects the latest backup from the first repository where backups exist, checking in configuration order (repo1 before repo2).

```
pgbackrest --stanza=demo restore
pgbackrest --stanza=demo --repo=2 --set=20150131-153358F_20150131-153401I restore
```

- `--set` (default `latest`) names a backup label.
- `--repo` forces a repository.
- For `--type=time` or `--type=lsn`, give `--target`. Without `--set`, repositories are checked in order for a backup containing the target; if none matches, the latest backup from the first repository is used for time, while no backup is selected for lsn.
- For other PITR types such as `xid`, `--set` must be given if the target is before the latest backup.
- Replication slots are not restored, per PostgreSQL's recommendation.

pgBackRest does not start PostgreSQL after writing the recovery settings, so you can inspect `postgresql.auto.conf` before starting the cluster. It writes `restore_command` to call `archive-get`.

## Checked

2026-11-08: default backup selection, --set and --repo, PITR target rules, replication slot exclusion and the no-automatic-start note confirmed in the Command Reference restore section and the User Guide. Partial reads: the User Guide, Command Reference and Configuration pages are long, so only the sections relevant to this skill were read, not every page end to end.

Method: documentation only; no commands were run.
