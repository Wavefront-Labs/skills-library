---
id: computing-software.database-administration.patroni.patroni-generate-and-validate-config
name: patroni-generate-and-validate-config
category: computing-software
field: database-administration
product: patroni
tags: [patroni, configuration, validation, generate-config, cli]
level: practitioner
status: docs-checked
description: "Use patroni --generate-sample-config, --generate-config and --validate-config to create and check YAML."
sources:
  - https://patroni.readthedocs.io/en/latest/patroni_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: create and verify a local configuration without hand-writing it.

```
patroni --generate-sample-config [configfile]
patroni --generate-config [--dsn DSN] [configfile]
patroni --validate-config [configfile] [--ignore-listen-port | -i] [--print | -p]
```

- Sample: values come from the environment configuration, else Patroni defaults, else the string `#FIXME` for values you must set. Listen and connect addresses default to the hostname's IP with ports 5432 (Postgres) and 8008 (REST API). The rewind authentication user is defined only if the PostgreSQL binary version is 11+.
- `--generate-config`: builds config from a running local PostgreSQL, using the DSN (takes precedence) or libpq environment variables; the password is prompted if absent. GUCs map to `scope` (cluster_name), `postgresql.listen`, `postgresql.datadir`, `postgresql.parameters` (archive_command, restore_command, hba_file, ident_file, etc.) and `bootstrap.dcs` (all others). `name` comes from `PATRONI_NAME` or the hostname; `bin_dir`, `pg_hba` and `pg_ident` are gathered from the instance.
- `--validate-config`: prints failed checks. Without a file, it reads `PATRONI_CONFIG_VARIABLE` or the environment. `-i` ignores bind failures for ports already in use; `-p` prints the validated local config including environment overrides.

If no configfile is given for generation, output goes to stdout. Release 4.1.5 fixed validation of `thread_stack_size` and accepting `quorum` and boolean-like strings for `synchronous_mode`.

## Checked

2026-11-03. Confirmed against patroni_configuration (Patroni configuration page): `--generate-sample-config`, `--generate-config [--dsn]`, `--validate-config` options, the `#FIXME` placeholder, GUC mapping and PATRONI_NAME behaviour; release 4.1.5 note against the release notes.

Method: documentation only; no commands were run.
