---
id: computing-software.systems-network-administration.syncthing.cli-subcommands-and-exit-codes
name: cli-subcommands-and-exit-codes
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, cli, subcommands, exit-codes]
level: practitioner
status: docs-checked
description: "Use the syncthing cli, generate, device-id, paths, upgrade and debug subcommands, and read process exit codes."
sources: ["https://docs.syncthing.net/users/syncthing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subcommands and exit codes

## Subcommands
`serve` (default), `cli`, `browser`, `decrypt`, `device-id`, `generate`, `paths`, `upgrade`, `version` and `debug`.

- `generate` creates the initial device ID and default configuration explicitly, and can set the GUI user and password (`--gui-user`, `--gui-password=<password|->`). It leaves an existing device certificate alone; an existing config is validated and updated to the latest schema, including defaults for new options.
- `device-id` and `paths` are subcommands that take the common options (the page gives their synopsis only).
- `decrypt` works on offline data, without Syncthing running.
- `upgrade` supports `--check-only` (only indicate whether an upgrade is available) and `--from=<url>`.
- `debug` offers data analysis and repair (`reset-database`, `database-statistics`, `database-counts`, `database-file`). Some of its commands access the database directly and can only work when Syncthing is not running. This is different from `cli debug`, which uses the REST API.

## cli groups
`syncthing cli` talks to a running instance over REST and handles authentication for you:
- `config` to get or set values in the same structure as the JSON or XML config
- `show` for properties and status (raw JSON)
- `operations` for restart, shutdown, upgrades and per-folder actions, and default ignore patterns
- `errors` to list or clear pending errors
- `debug` for diagnostics
- `-` reads further commands from stdin until EOF or an invalid command

Use `--help` at any level to explore; the groups are partly generated from the running instance.

## Exit codes
| Code | Meaning |
|---|---|
| 0 | success or shutdown |
| 1 | error |
| 2 | upgrade not available |
| 3 | restarting |
| 4 | upgrading |

Codes over 125 are usually returned by the shell, binary loader or default signal handler. On Unix, 128+N usually means signal N, for example 128 + 9 (SIGKILL) = 137.

## Checked
2026-11-04. Read Command Line Operation: subcommand list from the synopsis, `generate` behaviour, `upgrade` options, the `debug` subcommands and the cli/debug distinction, the cli top-level groups including `-`, and the exit-code table with the signal note. The cli-commands include page returned 404, so it was dropped from sources. Removed the claims about what `device-id` and `paths` print, which the page does not state.
Method: documentation only; no commands were run.
