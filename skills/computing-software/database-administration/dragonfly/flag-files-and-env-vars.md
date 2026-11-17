---
id: computing-software.database-administration.dragonfly.flag-files-and-env-vars
name: flag-files-and-env-vars
category: computing-software
field: database-administration
product: dragonfly
tags: [server-flags, dfly-env-vars, flagfile, helpfull, dragonfly]
level: practitioner
status: docs-checked
description: "The four ways to configure Dragonfly flags (command line, flag file, DFLY_ environment variables, CONFIG SET) and how to list flags."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dragonfly flags can be set four ways:

1. Command line arguments: `dragonfly --port=6379`.
2. A file: `dragonfly --flagfile=path_to_flags/flags.txt`.3. Environment variables: prefix `DFLY_` plus the flag name, for example `export DFLY_port=6379`. The name is case sensitive.
4. At runtime with `CONFIG SET`. Not all flags can be changed at runtime.

Discovery: `dragonfly --helpfull` lists every flag; `--help=substring` shows flags whose name, description or path contains the substring.

Selected defaults from the flag reference:

| Flag | Default |
| --- | --- |
| `port` | 6379 |
| `dbnum` | 16 |
| `maxclients` | 64000 |
| `maxmemory` | 0 (determined automatically) |
| `cache_mode` | false |
| `proactor_threads` | 0 (one per CPU core) |
| `bind` | empty (all interfaces, not advised) |

`requirepass` can also be supplied through the `DFLY_PASSWORD` environment variable when the flag is empty.

## Checked

2026-11-04: confirmed against the Server Configuration Flags page (four methods, --helpfull and --help=substring, every default in the table). Removed the claim that `--flagfile` takes a comma-separated list of files, which the page does not state.
Method: documentation only; no commands were run.
