---
id: computing-software.database-administration.pgbackrest.multiple-repositories
name: multiple-repositories
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, multiple-repositories, repo-option, redundancy, archive-push]
level: advanced
status: docs-checked
description: "Run several repositories side by side and know which commands need --repo."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: combine a fast local repository with a redundant remote one.

Configure indexed repositories (`repo1-`, `repo2-`, ...). A local repository gives fast restores while a remote one gives redundancy.

Behavior from the guide:

- `stanza-create` and `stanza-upgrade` work on all repositories automatically; commands such as `stanza-delete` require `--repo`.
- `--repo` is not required when only repo1 is configured, for backward compatibility, but is required if a single repository is configured as, for example, repo2, so adding another later does not break commands.
- Unqualified `backup` goes to the highest priority repository (repo1) unless `--repo` is given. Schedule backups individually per repository, since types and retention often differ.
- `restore` must specify a repository when needed; the docs advise choosing one with low latency or cost even if recovery is slower, and say only restore testing shows which is most efficient.
- `archive-push` always pushes WAL to all repositories. If one is unreachable, the others still receive WAL, but only with `archive-async=y`; otherwise they get at most one segment ahead.
- If WAL cannot reach any repository, PostgreSQL will not remove it from pg_wal, which may fill the volume.

```
pgbackrest --stanza=demo --repo=2 backup
```

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html) (Multiple Repositories). Nothing needed removing. 

Method: documentation only; no commands were run.
