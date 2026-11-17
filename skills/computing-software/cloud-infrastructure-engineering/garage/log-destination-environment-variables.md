---
id: computing-software.cloud-infrastructure-engineering.garage.log-destination-environment-variables
name: log-destination-environment-variables
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [garage-log-to-syslog, garage-log-to-journald, garage-log-format, no-color]
level: practitioner
status: docs-checked
description: "Send Garage logs to syslog or journald, emit JSON lines, or disable colors with environment variables."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
  - https://garagehq.deuxfleurs.fr/documentation/quick-start/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Some settings exist only as environment variables, not in `garage.toml`:

- `GARAGE_LOG_TO_SYSLOG` (since v0.9.4): set to `1` or `true` to send logs to syslog through the libc function instead of stderr.
- `GARAGE_LOG_TO_JOURNALD` (since v1.2.0): set to `1` or `true` to use the native systemd-journald protocol.
- `GARAGE_LOG_FORMAT` (since v2.5.0): set to `json` to print one JSON object per line to stderr. It cannot currently be combined with syslog or journald; when either is set it takes precedence and the format variable is ignored.
- `NO_COLOR` (since v2.4.0): set to `1` or `true` to remove ANSI color codes.

Verbosity still comes from `RUST_LOG`, with levels `error`, `warn`, `info` (default), `debug` and `trace`.

Variables that override file values: `GARAGE_ALLOW_WORLD_READABLE_SECRETS`, `GARAGE_RPC_SECRET` and `GARAGE_RPC_SECRET_FILE`, `GARAGE_ADMIN_TOKEN` and `GARAGE_ADMIN_TOKEN_FILE`, and the metrics token variables.

Version summary: syslog support dates from v0.9.4, journald from v1.2.0, JSON format from v2.5.0 and NO_COLOR from v2.4.0.

## Checked

2026-11-04. Read the Configuration file format and Quick Start pages. Confirmed the four logging variables with their since-versions and precedence rule, the RUST_LOG levels and default and the list of override variables. Removed the systemd unit sentence, which neither page states.
Method: documentation only; no commands were run.
