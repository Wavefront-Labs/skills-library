---
id: computing-software.database-administration.pgbackrest.checksum-page-option
name: checksum-page-option
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, checksum-page, data-checksums, corruption, backup]
level: advanced
status: docs-checked
description: "What checksum-page and checksum-page-error do on backup, expire and restore."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: detect page corruption without surprise failures.

`checksum-page` directs pgBackRest to validate all data page checksums while backing up a cluster. It is automatically enabled when data page checksums are enabled on the cluster.

Failures in checksum validation do not abort a backup by default. Warnings are emitted in the log (and to the console at default settings) and the list of invalid pages is stored in the backup manifest.

```
pgbackrest --stanza=demo --no-checksum-page backup
```

`checksum-page-error` appears in three commands with different meanings:

- backup (default `n`): when enabled together with checksum-page, a validation failure terminates the backup.
- expire (default `y`): expire stops with an error before changing anything if the oldest retained backup would contain checksum errors; if disabled, it proceeds with a warning. Using `--set` lets expire proceed regardless, with a warning.
- restore: see the restore command options.

Because pages are reported rather than fatal, scan the log after each backup. For repository-wide checks of file checksums use the `verify` command.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest Command Reference (pgbackrest.org/command.html). Removed: the restore default for checksum-page-error. 

Method: documentation only; no commands were run.
