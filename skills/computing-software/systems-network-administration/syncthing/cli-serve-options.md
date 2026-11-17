---
id: computing-software.systems-network-administration.syncthing.cli-serve-options
name: cli-serve-options
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, cli, serve-options, log-file]
level: practitioner
status: docs-checked
description: "Run syncthing serve with home and data directories, logging flags, GUI overrides and equivalent ST environment variables."
sources: ["https://docs.syncthing.net/users/syncthing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serve options

`syncthing` with no subcommand means `serve`. The flags below list their environment variable on the page.

## Locations
- `--home=<dir>` (`$STHOMEDIR`) sets configuration and data together.
- `--config=<dir>` (`$STCONFDIR`) and `--data=<dir>` (`$STDATADIR`) split them. Use both together.

## GUI
- `--gui-address=<address>` (`$STGUIADDRESS`) takes `0.0.0.0:8384` or a URL. Schemes: `http`, `https`, `unix`, `unixs`.
- `--gui-apikey=<key>` (`$STGUIAPIKEY`) overrides the API key.
- `--no-browser` stops the browser opening.

## Logging
- `--log-file=<name>` (`$STLOGFILE`), with `-` meaning stdout.
- `--log-level=<level>` (`$STLOGLEVEL`): DEBUG, INFO, WARN or ERROR.
- `--log-max-size` (bytes, `0` disables rotation) and `--log-max-old-files`.
- `--log-format-timestamp`, `--[no-]log-format-level-string`, `--[no-]log-format-level-syslog`.
- `--audit` writes events to `audit-YYYYMMDD-HHMMSS.log`. `--auditfile` picks a file, `-` stdout or `--` stderr.

## Behaviour
- `--no-restart` means Syncthing is not restarted when it exits; the monitor process still runs to handle crashes and write log files.
- `--no-upgrade` disables automatic upgrades.
- `--paused` or `--unpaused` start with everything paused or unpaused.
- `--allow-newer-config` tries to load a config file written by a newer program version instead of failing immediately.
- `--no-port-probing` does not look for unused random ports for the GUI and listen address when generating an initial configuration or starting for the first time.
- `--db-maintenance-interval` and `--db-delete-retention-interval` take Go durations.

## Checked
2026-11-04. Read Command Line Operation (common options and serve options): every flag, the `ST*` variable names given, the GUI address schemes, log-file `-` for stdout, log levels, log rotation, audit file forms, `--no-restart` wording, pause flags and Go-duration interval format. Removed the closing `syncthing paths` hint, which the page does not describe.
Method: documentation only; no commands were run.
