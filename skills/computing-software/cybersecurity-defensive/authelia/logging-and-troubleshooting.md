---
id: computing-software.cybersecurity-defensive.authelia.logging-and-troubleshooting
name: logging-and-troubleshooting
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, logging, log-level, json-logs, sighup, troubleshooting, log-rotation]
level: practitioner
status: docs-checked
description: "Configure Authelia log level, format and file output with SIGHUP rotation, and collect the logs the maintainers ask for in a bug report."
sources:
  - https://www.authelia.com/configuration/miscellaneous/logging/
  - https://www.authelia.com/reference/guides/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
log:
  level: 'info'
  format: 'text'
  file_path: '/config/authelia.log'
  keep_stdout: true
```

- `level` is `trace`, `debug`, `info`, `warn` or `error`. `trace` is very noisy and also exposes `/debug/vars` and `/debug/pprof/`, so do not leave it on in production.
- `format` is `text` or `json`.
- `file_path` writes logs to a file; otherwise they go to standard output. Supported replacements are `%d` (RFC 3339 date) and `{datetime}`, optionally with a Go layout as `{datetime:<layout>}`. Rotate or truncate the file, because debug and trace grow quickly.
- `keep_stdout` (default false) keeps writing to standard output as well as the file; otherwise logs go only to `file_path`.
- Sending `SIGHUP` makes Authelia close, reopen and truncate the log file, which suits log-rotation services that must force a reopen.

For a bug report the troubleshooting guide asks for complete logs with the level at `debug` at minimum, if not `trace`, from the log severity line ("Log severity set to ...") until the problem occurs. Truncated logs are accepted only if they show more than 1 minute of logs before the issue, the log severity line, the listening line and the 10 lines after it, the lines between those (including the starting line), and any related warning or error. With `file_path` set and `keep_stdout` off, the console logs and file logs must be joined; with `keep_stdout` on, the console logs suffice.

Check: raise the level to debug, reproduce, and confirm the starting and listening lines are present.

## Checked

2026-11-08. Read the full Authelia Log page and the Troubleshooting guide. Confirmed level values, trace endpoint exposure, format, file_path replacements, keep_stdout, SIGHUP behaviour and the log submission rules (debug minimum, truncation rules, stdout and file joining). Removed disable_timestamp, which the Log page does not list. Fixed trailing commas in the sources list.

Method: documentation only; no commands were run.
