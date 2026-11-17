---
id: computing-software.database-administration.pgbackrest.info-command
name: info-command
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, info, backup-status, json, stanza-status]
level: intro
status: docs-checked
description: "Read backup and archive status with info, including text versus JSON output and detail levels."
sources:
  - https://pgbackrest.org/command.html
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: see what is in the repository.

`pgbackrest info` operates on all stanzas or one with `--stanza`. Text output is the default and is subject to change between releases. For machine-readable output use `--output=json`: it holds far more information and is kept stable unless a bug is found.

```
pgbackrest info
pgbackrest --stanza=demo --output=json info
pgbackrest --stanza=demo --set=20261015-070756F info
```

Options:

- `--set` shows one backup in full, including its complete backup reference list, database list and annotations.
- `--detail-level=progress` limits output to progress information and skips all checks except availability of the stanza, which speeds up execution.
- `--repo` limits to one repository; the WAL min/max is otherwise reported across all repositories.
- `--type` filters by backup type.

Stanza status is `ok` when pgBackRest is functioning normally. With multiple repositories, `mixed` means the stanza is unhealthy on one or more repositories and each repository's state is detailed. `other` is used for an unknown repository error, with full details shown.

`backup/expire running` and `restore running` appear beside the status while those commands run. When run without `--stanza`, info reads encryption settings only from the global section.

## Checked

2026-11-08: info options, output types, detail levels, stanza status values (ok, mixed, other) and the running-command markers confirmed in the Command Reference info section; annotations and the encryption-from-global note confirmed in the User Guide. Partial reads: the User Guide, Command Reference and Configuration pages are long, so only the sections relevant to this skill were read, not every page end to end.

Method: documentation only; no commands were run.
