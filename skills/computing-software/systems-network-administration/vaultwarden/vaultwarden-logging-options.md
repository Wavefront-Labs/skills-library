---
id: computing-software.systems-network-administration.vaultwarden.vaultwarden-logging-options
name: vaultwarden-logging-options
category: computing-software
field: systems-network-administration
product: vaultwarden
tags: [vaultwarden, logging, log-file, log-level, extended-logging, syslog, docker-logs]
level: intro
status: docs-checked
description: "Configure Vaultwarden logging with LOG_FILE, LOG_LEVEL, EXTENDED_LOGGING and USE_SYSLOG, and read container logs."
sources: ["https://github.com/dani-garcia/vaultwarden/wiki/Logging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vaultwarden logging

- `LOG_FILE`: write logs to a file (supported since 1.5.0). Needed by Fail2Ban.
- `LOG_LEVEL`: `trace`, `debug`, `info` (default), `warn`, `error` or `off`. It only takes effect when `EXTENDED_LOGGING=true`.
- `EXTENDED_LOGGING`: must be `true` for `LOG_LEVEL` and `USE_SYSLOG` to work.
- `USE_SYSLOG`: log to syslog; requires `EXTENDED_LOGGING=true`.
- In Docker, `docker logs <container-name>` shows the console output.

Security note from the hardening guide: Vaultwarden truncates logged query strings to 30 characters, but redact the `access_token` query parameter at the reverse proxy or log store as well.

The wiki links a logrotate example for rotating the log file.

## Checked

2026-11-03. Confirmed against the Vaultwarden wiki (https://github.com/dani-garcia/vaultwarden/wiki) by reading: Logging and Hardening-Guide (30-character query truncation).
Removed or reworded: generic closing advice about debug level and the unconfirmed 'mount a volume' tip.
Method: documentation only; no commands were run.
