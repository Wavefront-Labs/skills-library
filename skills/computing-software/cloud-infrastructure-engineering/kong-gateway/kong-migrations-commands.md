---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.kong-migrations-commands
name: kong-migrations-commands
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, kong-migrations, bootstrap, migrations-finish, database, cli]
level: practitioner
status: docs-checked
description: "The kong migrations subcommands bootstrap, up, finish, list and reset with their flags, and the --run-migrations option on kong start."
sources:
  - https://developer.konghq.com/gateway/cli/reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kong migrations commands

| Command | Purpose |
|---|---|
| `kong migrations bootstrap` | set up the database and run all migrations |
| `kong migrations up` | run any new migrations |
| `kong migrations finish` | complete pending migrations after `up` |
| `kong migrations list` | list executed migrations |
| `kong migrations reset` | erase all database data and delete schemas (destructive) |

The CLI reference lists these options for `kong migrations`:
- `-y, --yes`
- `-q, --quiet`
- `-f, --force`
- `--db-timeout`
- `--lock-timeout` (default 60)
- `-c, --conf`
- `-p, --prefix`

`kong start` and `kong restart` also take `--run-migrations` (boolean), `--db-timeout` and `--lock-timeout`.

`finish` runs after `up`. For ordering and intermediate stops during an upgrade, follow the version-specific upgrade guide.

## Checked

2026-11-04. Confirmed against the CLI reference: the five subcommand descriptions, the option list and the `--lock-timeout` default of 60, and `--run-migrations` on `kong start` and `kong restart`. Reworded the claim that all five subcommands take identical flags, since the page lists the options once for the whole command.
Method: documentation only; no commands were run.
