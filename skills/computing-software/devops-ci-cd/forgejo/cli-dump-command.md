---
id: computing-software.devops-ci-cd.forgejo.cli-dump-command
name: cli-dump-command
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [forgejo-dump, dump-zip, skip-flags, dump-type]
level: practitioner
status: docs-checked
description: "Create a single archive of Forgejo files and database with forgejo dump and its skip and format options."
sources:
  - https://forgejo.org/docs/latest/admin/command-line/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`forgejo dump` compresses all related files and the database into one archive. The help text says it can serve as a backup and to capture a server image to send to a maintainer.

Useful options:

- `--file`, `-f`: output name; default is `forgejo-dump-<timestamp>.zip`; `-` writes to stdout.
- `--type`: zip (default), tar, tar.sz, tar.gz, tar.xz, tar.bz2, tar.br, tar.lz4 or tar.zst.
- `--database`, `-d`: SQL syntax for the database dump, one of sqlite3, mysql, postgres.
- `--tempdir`, `-t`: temporary directory.
- `--verbose`, `-V` and `--quiet`, `-q`: control output.
- Skip flags: `--skip-repository` (`-R`), `--skip-log` (`-L`), `--skip-custom-dir`, `--skip-lfs-data`, `--skip-attachment-data`, `--skip-package-data`, `--skip-index`, `--skip-repo-archives`.

Like every subcommand it accepts the global options `--config`/`-c`, `--custom-path`/`-C` and `--work-path`/`-w`, defaulting to `{WorkPath}/custom/conf/app.ini`.

Example: `forgejo dump --type tar.zst --file /path/to/backups/forgejo.tar.zst --skip-log`. Remember that the backup guide recommends stopping Forgejo for a consistent backup and says Forgejo recommends no particular backup tool.

By default the archive is a zip file named with a timestamp, and the help describes the command as compressing all related files and the database.

## Checked

2026-11-04. Confirmed against the Forgejo command-line page (dump help text): every option, short flag, the type list, the zip default and the file name default. The backup guide confirms the stop-Forgejo recommendation. Nothing removed.

Method: documentation only; no commands were run.
