---
id: computing-software.database-administration.pgbackrest.stanza-create-and-upgrade
name: stanza-create-and-upgrade
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, stanza-create, stanza-upgrade, repository, major-upgrade]
level: practitioner
status: docs-checked
description: "Initialise a stanza in each repository and re-point it after a PostgreSQL major version upgrade."
sources:
  - https://pgbackrest.org/command.html
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: create and maintain the stanza metadata.

`stanza-create` writes the backup and archive structures for the stanza in each configured repository. It is safe to rerun: for an existing valid stanza it reports that the stanza already exists and is valid, then moves to the next repository. With several repositories it processes all of them automatically.

```
pgbackrest --stanza=demo --log-level-console=info stanza-create
```

Repository encryption settings cannot be changed once the repository is configured and the stanza is created and checked, so choose them before `stanza-create`.

`stanza-upgrade` is run after a PostgreSQL major version upgrade. Order from the user guide:

1. Stop the old cluster and run pg_upgrade.
2. Set `pg1-path` (and `pg2-path` on a repository host) to the new data directory on every host.
3. Run stanza-upgrade before starting the new cluster; add `--no-online` if the database is offline.
4. Start the cluster and run `check`.

```
pgbackrest --stanza=demo --no-online stanza-upgrade
```

With more than one repository the stanza is upgraded in each. The guide then runs a full backup on the new cluster; an incr or diff request is changed to full automatically.

## Checked

2026-11-08: stanza-create and stanza-upgrade behaviour and options confirmed in the Command Reference; the upgrade order, encryption note and automatic full backup confirmed in the User Guide. Changed: two sentences reworded to match the guide. Partial reads: the User Guide, Command Reference and Configuration pages are long, so only the sections relevant to this skill were read, not every page end to end.

Method: documentation only; no commands were run.
