---
id: computing-software.database-administration.pgbackrest.stanza-delete
name: stanza-delete
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, stanza-delete, repository, cleanup, stop]
level: advanced
status: docs-checked
description: "Permanently remove a stanza's backups and archive from a repository, one repository at a time."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: delete a stanza without leaving a live cluster writing to it.

Warning: this permanently removes all backups and archives for the stanza from the repository.

Steps:

1. Shut down the PostgreSQL cluster for the stanza, or use `--force` to override.
2. Run `stop` on the host where `stanza-delete` will run.
3. Run `stanza-delete`.
4. Remove the stanza from all configuration files and environment variables; that is the user's job.

```
pg_ctlcluster 17 demo stop
pgbackrest --stanza=demo stop
pgbackrest --stanza=demo --repo=1 stanza-delete
```

A stanza is deleted from one repository at a time; repeat with `--repo` for each.

On versioned object storage, a deleted stanza can still be read as it was before deletion using `--repo-target-time`. Afterwards `info` on the repository reports `status: error (missing stanza path)`.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Command Reference (pgbackrest.org/command.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html) (Delete a Stanza). Removed: the claim that stanza-delete works while stopped and a repeated paragraph. 

Method: documentation only; no commands were run.
