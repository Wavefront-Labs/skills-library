---
id: computing-software.database-administration.pgbackrest.multiple-stanzas-shared-repository
name: multiple-stanzas-shared-repository
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, stanza, repository-host, shared-repository, check]
level: practitioner
status: docs-checked
description: "Share a repository host among several stanzas, each with its own archive and backups."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: back up unrelated clusters to one repository.

Each cluster gets its own stanza so its backups and archive are stored separately. The repository host lists every stanza and its database host:

```
[demo]
pg1-host=pg-primary
pg1-path=/path/to/pgdata

[demo-alt]
pg1-host=pg-alt
pg1-path=/path/to/pgdata

[global]
process-max=3
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
```

Each database host uses its own stanza name in its config and in `archive_command`:

```
archive_command = 'pgbackrest --stanza=demo-alt archive-push %p'
```

Then create the stanza and check:

```
pgbackrest --stanza=demo-alt --log-level-console=info stanza-create
pgbackrest --log-level-console=info check
```

Run on the database host, `check` without a stanza covers the stanza in its configuration. Run from the repository host, it checks all stanzas in turn, reporting an archived WAL segment for each.

Pick stanza names that describe the function of the cluster, since the name serves primary and replicas alike.

Use `--stanza` on commands run from the repository host when you want to act on one stanza only; otherwise commands such as `check` cover all configured stanzas.

## Checked

2026-11-08: the repository host configuration, per-host archive_command, stanza-create and check behaviour and the stanza naming advice confirmed in the User Guide Multiple Stanzas and Quick Start sections. Partial reads: the User Guide, Command Reference and Configuration pages are long, so only the sections relevant to this skill were read, not every page end to end.

Method: documentation only; no commands were run.
