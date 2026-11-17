---
id: computing-software.database-administration.pgbackrest.verify-command
name: verify-command
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, verify, repository, integrity, backup-set]
level: advanced
status: docs-checked
description: "Check that backups and archives in a repository are valid with verify."
sources:
  - https://pgbackrest.org/command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: confirm repository contents before you need them.

`verify` determines whether the backups and archives in a repository are valid.

```
pgbackrest --stanza=demo --output=text verify
pgbackrest --stanza=demo --set=20150131-153358F_20150131-153401I --verbose verify
```

Options:

- `--output`: `none` (default) or `text` to print verify information to stdout.
- `--set`: verify all database and archive files associated with the specified backup set.
- `--verbose` (default n): by default a minimal response with important information about errors; verbose adds what was successfully verified.

General options that matter for runtime: `process-max` (parallel file checks), `io-timeout`, `protocol-timeout` and `buffer-size`.

How it differs from `check`: check validates configuration and forces a WAL segment into the archive; verify determines whether the backups and archives already in the repository are valid.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Command Reference (pgbackrest.org/command.html) (verify). Removed: the advice on scheduling verify and the remark about restore testing. 

Method: documentation only; no commands were run.
