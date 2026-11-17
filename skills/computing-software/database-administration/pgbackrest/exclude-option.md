---
id: computing-software.database-administration.pgbackrest.exclude-option
name: exclude-option
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, exclude, backup, delta, pgdata]
level: practitioner
status: docs-checked
description: "Exclude files and directories from a backup with --exclude, with the trailing slash rule and the delta restore caveat."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: skip files that should not be backed up.

`exclude` is a list option, repeated per pattern or set several times in the file. All exclusions are relative to `$PGDATA`.

- With a trailing `/`, only files in that directory are excluded; `--exclude=junk/` excludes the files in `$PGDATA/junk` but keeps the directory itself.
- Without a trailing `/`, the file may match exactly or match with `/` appended; `--exclude=junk` excludes the `$PGDATA/junk` directory and everything in it.

```
[demo]
pg1-path=/path/to/pgdata
exclude=junk/
```

Cautions from the docs:

- It is very easy to exclude something critical and make the backup inconsistent. Test your restores.
- Excluded files are logged at info level with the matching rule; audit that list for surprises.
- Exclusions are not honored on delta restores: any files or directories that the backup excluded will be removed on delta restore.
- Do not use it to exclude PostgreSQL logs. Move logs out of PGDATA with the `log_directory` setting instead, which also preserves them after a restore.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest Command Reference (pgbackrest.org/command.html). Nothing needed removing. 

Method: documentation only; no commands were run.
