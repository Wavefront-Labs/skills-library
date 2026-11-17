---
id: computing-software.database-administration.pgbackrest.repo-get-and-repo-ls
name: repo-get-and-repo-ls
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, repo-get, repo-ls, repository, troubleshooting]
level: practitioner
status: docs-checked
description: "Inspect repository files on any repository type with repo-ls and repo-get."
sources:
  - https://pgbackrest.org/command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: look inside a repository for troubleshooting.

Both commands work on any supported repository type and are for administration, investigation and testing; neither is part of a normal setup. With multiple repositories they default to the highest priority one unless `--repo` is given.

`repo-ls` is like `ls`. It takes a path, absolute or relative to `repo-path`. Text output prints one name per line; `--output=json` gives name, type (file, path or link), size in bytes and last-modified time for files. `--filter` applies a regular expression to names before output, for example `--filter="(F|D|I)$"` to show backup labels.

```
pgbackrest --stanza=demo repo-ls backup/demo
pgbackrest --stanza=demo --output=json repo-ls backup/demo
```

`repo-get` is like `cat` and needs a fully qualified file name. If the repository is encrypted it decrypts automatically. Files are not automatically decompressed, so pipe through the matching tool, such as `gzip -d`. `--ignore-missing` exits 1 for a missing source file without raising an error.

```
pgbackrest --stanza=demo repo-get backup/demo/backup.info
```

## Checked

2026-11-08: repo-ls and repo-get behaviour, --filter, --output=json fields, --ignore-missing and the multi-repository default confirmed in the Command Reference. Partial reads: the User Guide, Command Reference and Configuration pages are long, so only the sections relevant to this skill were read, not every page end to end.

Method: documentation only; no commands were run.
