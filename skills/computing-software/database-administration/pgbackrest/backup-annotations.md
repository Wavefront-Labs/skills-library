---
id: computing-software.database-administration.pgbackrest.backup-annotations
name: backup-annotations
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, annotate, annotation, backup, info]
level: practitioner
status: docs-checked
description: "Attach key/value notes to a backup with --annotation or the annotate command and read them from info."
sources:
  - https://pgbackrest.org/command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: record context with each backup.

An annotation is a key/value pair stored with a backup. Set it during the backup with the `annotation` option, or later with the `annotate` command.

```
pgbackrest --stanza=demo --annotation=source=cron --annotation=ticket=1234 backup
pgbackrest --stanza=demo --set=20261015-070800F --annotation=keep=yes annotate
```

`annotation` is a key/value option and can be repeated. Annotations are shown in the text output of `info` only when a backup is chosen with `--set`, and they always appear in the JSON output, which suits monitoring scripts:

```
pgbackrest --stanza=demo --output=json info
```

The `annotate` command adds, modifies or removes annotations on an existing backup, and `--set` names the backup to annotate (for example `20150131-153358F_20150131-153401I`). The docs' own example value is `source="Sunday backup for website database"`.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Command Reference (pgbackrest.org/command.html) and the pgBackRest Configuration Reference (pgbackrest.org/configuration.html). Removed: the claim about removing an annotation with an empty value (--annotation=key=), which is not on the fetched pages, and a filler sentence. 

Method: documentation only; no commands were run.
