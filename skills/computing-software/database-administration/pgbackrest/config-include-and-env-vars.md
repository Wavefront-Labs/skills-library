---
id: computing-software.database-administration.pgbackrest.config-include-and-env-vars
name: config-include-and-env-vars
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, configuration, environment-variables, conf-d, config-include-path]
level: practitioner
status: docs-checked
description: "Split configuration across files with config-include-path and override options through PGBACKREST_ environment variables."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: layer configuration without editing one big file.

Three options control file loading: `config` (the main file), `config-include-path` (a directory, conf.d by default beside the main file) and `config-path` (the base for both). Files in the include directory with the `.conf` extension are concatenated with the main file, resulting in one configuration.

```
/etc/pgbackrest/pgbackrest.conf
/etc/pgbackrest/conf.d/demo.conf
```

Environment variables: prefix `PGBACKREST_` plus the option name in capitals with `-` replaced by `_`.

```
export PGBACKREST_STANZA=demo
export PGBACKREST_REPO1_RETENTION_FULL=3
pgbackrest backup
```

Command-line options override environment options, which override config file options.

After `stanza-delete`, remove the stanza from all configuration files and environment variables; that is the user's job.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Command Reference (pgbackrest.org/command.html) (Configuration and --config-include-path). Removed: the claim about packaging-dropped per-stanza files, the section-precedence claim and the sensitive-values remark; the precedence line now follows the command reference. 

Method: documentation only; no commands were run.
